"""
音乐视图
"""
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count
from django.utils import timezone
from .models import Song, StarSong, BuySong
from .serializers import SongSerializer, SongCreateSerializer, StarSongSerializer, BuySongSerializer
from apps.users.models import LoginLog
from apps.audit.models import CheckSongLog


class SongViewSet(viewsets.ModelViewSet):
    """歌曲视图集"""
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    
    def get_queryset(self):
        """根据用户类型和权限返回不同的查询集"""
        queryset = Song.objects.select_related('song_singer').all()
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(song_name__icontains=search) |
                Q(song_singer__user_name__icontains=search)
            )
        
        # 按歌手筛选
        singer_id = self.request.query_params.get('singer_id', None)
        if singer_id:
            queryset = queryset.filter(song_singer_id=singer_id)
        
        # 按价格筛选
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        if price_min:
            queryset = queryset.filter(song_price__gte=price_min)
        if price_max:
            queryset = queryset.filter(song_price__lte=price_max)
        
        # 普通用户只能看到已上架的歌曲
        if not self.request.user.is_authenticated or self.request.user.user_type == 0:
            queryset = queryset.filter(is_active=True)
        # 歌手可以看到自己的所有歌曲
        elif self.request.user.user_type == 1:
            queryset = queryset.filter(
                Q(is_active=True) | Q(song_singer=self.request.user)
            )
        # 管理员可以看到所有歌曲
        
        return queryset.order_by('-song_createtime')
    
    def get_serializer_class(self):
        """根据操作选择不同的序列化器"""
        if self.action == 'create':
            return SongCreateSerializer
        return SongSerializer
    
    def get_permissions(self):
        """权限控制"""
        if self.action in ['list', 'retrieve']:
            # 列表和详情允许所有用户访问
            return [permissions.AllowAny()]
        elif self.action == 'create':
            # 创建需要歌手权限
            return [permissions.IsAuthenticated()]
        else:
            # 更新和删除需要歌手权限（只能操作自己的歌曲）或管理员权限
            return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        """创建歌曲，自动创建审核记录"""
        song = serializer.save()
        # 创建审核记录
        CheckSongLog.objects.create(
            check_song=song,
            check_song_name=song.song_name,
            check_song_cover=str(song.song_cover) if song.song_cover else '',
            check_song_file=str(song.song_file),
            check_song_duration=song.song_duration,
            check_song_price=song.song_price,
            check_status=0  # 待审核
        )
    
    def perform_update(self, serializer):
        """更新歌曲（需要重新审核）"""
        song = serializer.save()
        song.is_active = False  # 修改后需要重新审核
        song.save()
        # 创建新的审核记录
        CheckSongLog.objects.create(
            check_song=song,
            check_song_name=song.song_name,
            check_song_cover=str(song.song_cover) if song.song_cover else '',
            check_song_file=str(song.song_file),
            check_song_duration=song.song_duration,
            check_song_price=song.song_price,
            check_status=0  # 待审核
        )
    
    def perform_destroy(self, instance):
        """删除歌曲（只有歌手本人或管理员可以删除）"""
        if self.request.user.user_type == 2 or instance.song_singer == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied('无权删除此歌曲')
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def star(self, request, pk=None):
        """收藏歌曲"""
        song = self.get_object()
        star_song, created = StarSong.objects.get_or_create(
            user=request.user,
            song=song
        )
        if created:
            return Response({
                'message': '收藏成功',
                'star_song': StarSongSerializer(star_song).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '已经收藏过该歌曲'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unstar(self, request, pk=None):
        """取消收藏"""
        song = self.get_object()
        star_song = StarSong.objects.filter(user=request.user, song=song).first()
        if star_song:
            star_song.delete()
            return Response({'message': '取消收藏成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '未收藏该歌曲'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def buy(self, request, pk=None):
        """购买歌曲"""
        song = self.get_object()
        
        # 检查是否已购买
        if BuySong.objects.filter(user=request.user, song=song).exists():
            return Response({'error': '已经购买过该歌曲'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 免费歌曲不需要购买
        if song.song_price == 0:
            return Response({'error': '该歌曲是免费的，无需购买'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建购买记录
        buy_song = BuySong.objects.create(
            user=request.user,
            song=song,
            buy_price=song.song_price
        )
        
        return Response({
            'message': '购买成功',
            'buy_song': BuySongSerializer(buy_song).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_songs(self, request):
        """获取当前歌手上传的歌曲"""
        if request.user.user_type != 1:
            return Response(
                {'error': '只有歌手可以查看自己的歌曲'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        songs = Song.objects.filter(song_singer=request.user)
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def starred(self, request):
        """获取当前用户收藏的歌曲"""
        star_songs = StarSong.objects.filter(user=request.user).select_related('song')
        songs = [star_song.song for star_song in star_songs]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def bought(self, request):
        """获取当前用户购买的歌曲"""
        buy_songs = BuySong.objects.filter(user=request.user).select_related('song')
        songs = [buy_song.song for buy_song in buy_songs]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)


class SongStatisticsView(APIView):
    """歌曲统计视图（歌手端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, song_id=None):
        """获取歌曲统计数据"""
        if request.user.user_type != 1:
            return Response(
                {'error': '只有歌手可以查看统计数据'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if song_id:
            # 单个歌曲统计
            try:
                song = Song.objects.get(song_id=song_id, song_singer=request.user)
                star_count = song.starred_by.count()
                buy_count = song.bought_by.count()
                
                return Response({
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'star_count': star_count,
                    'buy_count': buy_count,
                    'total_revenue': float(song.song_price * buy_count),
                })
            except Song.DoesNotExist:
                return Response(
                    {'error': '歌曲不存在'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # 所有歌曲统计
            songs = Song.objects.filter(song_singer=request.user).annotate(
                star_count=Count('starred_by'),
                buy_count=Count('bought_by')
            )
            
            total_songs = songs.count()
            total_stars = sum(song.star_count for song in songs)
            total_buys = sum(song.buy_count for song in songs)
            total_revenue = sum(float(song.song_price * song.buy_count) for song in songs)
            
            return Response({
                'total_songs': total_songs,
                'total_stars': total_stars,
                'total_buys': total_buys,
                'total_revenue': total_revenue,
                'songs': [
                    {
                        'song_id': song.song_id,
                        'song_name': song.song_name,
                        'star_count': song.star_count,
                        'buy_count': song.buy_count,
                        'revenue': float(song.song_price * song.buy_count),
                    }
                    for song in songs
                ]
            })


