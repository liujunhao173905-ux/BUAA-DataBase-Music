"""
歌单视图
"""
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F, Max
from .models import Playlist, PlaylistSong, StarPlaylist
from .serializers import (
    SongSerializer,
    PlaylistSerializer, 
    PlaylistCreateSerializer,
    PlaylistUpdateSerializer,
    PlaylistSongSerializer,
    StarPlaylistSerializer
)
from apps.music.models import Song
from apps.audit.models import CheckPlaylistLog


class PlaylistViewSet(viewsets.ModelViewSet):
    """歌单视图集"""
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    
    def list(self, request, *args, **kwargs):
        """获取歌单列表，支持搜索和分页"""
        queryset = self.get_queryset()
        
        # 获取分页数据
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'data': {
                    'playlists': serializer.data,
                    'total': self.paginator.page.paginator.count
                }
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': {
                'playlists': serializer.data,
                'total': queryset.count()
            }
        })
    
    def get_queryset(self):
        """根据用户类型和权限返回不同的查询集"""
        queryset = Playlist.objects.select_related('playlist_creator').prefetch_related('songs__song')
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(playlist_name__icontains=search) |
                Q(playlist_creator__user_name__icontains=search)
            )
        
        # 按创建者筛选
        creator_id = self.request.query_params.get('creator_id', None)
        if creator_id:
            queryset = queryset.filter(playlist_creator_id=creator_id)
        
        # 普通用户只能看到已公开的歌单
        if not self.request.user.is_authenticated or self.request.user.user_type == 0:
            queryset = queryset.filter(is_active=True)
        # 用户可以看到自己的所有歌单
        elif self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(is_active=True) | Q(playlist_creator=self.request.user)
            )
        
        return queryset.order_by('-playlist_createtime')
    
    def get_serializer_class(self):
        """根据操作选择不同的序列化器"""
        if self.action == 'create':
            return PlaylistCreateSerializer
        elif self.action == 'update':
            return PlaylistUpdateSerializer
        return PlaylistSerializer
    
    def get_permissions(self):
        """权限控制"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        """创建歌单"""
        serializer.save()
    
    def perform_update(self, serializer):
        """更新歌单（需要重新审核）"""
        playlist = serializer.save()
        playlist.is_active = False  # 修改后需要重新审核
        playlist.save()
        # 创建新的审核记录
        CheckPlaylistLog.objects.create(
            check_playlist=playlist,
            check_playlist_name=playlist.playlist_name,
            check_playlist_cover=str(playlist.playlist_cover) if playlist.playlist_cover else '',
            check_playlist_intro=playlist.playlist_intro or '',
            check_status=0  # 待审核
        )
    
    def perform_destroy(self, instance):
        """删除歌单（只有创建者或管理员可以删除）"""
        if self.request.user.user_type == 2 or instance.playlist_creator == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied('无权删除此歌单')
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_song(self, request, pk=None):
        """向歌单添加歌曲"""
        playlist = self.get_object()
        
        # 检查权限
        if playlist.playlist_creator != request.user and request.user.user_type != 2:
            return Response(
                {'error': '只有歌单创建者可以添加歌曲'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        song_id = request.data.get('song_id')
        if not song_id:
            return Response(
                {'error': '需要提供song_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            song = Song.objects.get(song_id=song_id, is_active=True)
        except Song.DoesNotExist:
            return Response(
                {'error': '歌曲不存在或未上架'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 检查是否已添加
        if PlaylistSong.objects.filter(playlist=playlist, song=song).exists():
            return Response(
                {'error': '歌曲已在歌单中'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取当前最大排序值
        max_order = PlaylistSong.objects.filter(playlist=playlist).aggregate(
            max_order=Max('order')
        )['max_order'] or 0
        
        playlist_song = PlaylistSong.objects.create(
            playlist=playlist,
            song=song,
            order=max_order + 1
        )
        
        return Response({
            'message': '添加成功',
            'playlist_song': PlaylistSongSerializer(playlist_song).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def remove_song(self, request, pk=None):
        """从歌单移除歌曲"""
        playlist = self.get_object()
        
        # 检查权限
        if playlist.playlist_creator != request.user and request.user.user_type != 2:
            return Response(
                {'error': '只有歌单创建者可以移除歌曲'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        song_id = request.data.get('song_id')
        if not song_id:
            return Response(
                {'error': '需要提供song_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        playlist_song = PlaylistSong.objects.filter(
            playlist=playlist,
            song_id=song_id
        ).first()
        
        if playlist_song:
            playlist_song.delete()
            return Response({'message': '移除成功'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': '歌曲不在歌单中'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def check_song(self, request, pk=None):
        """检查某首歌曲是否在当前歌单中"""
        song_id = request.query_params.get('song_id')
        if not song_id:
            return Response({'error': '需要提供 song_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'error': '歌单不存在'}, status=status.HTTP_404_NOT_FOUND)

        exists = PlaylistSong.objects.filter(playlist=playlist, song_id=song_id).exists()
        return Response({'is_in_playlist': exists}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def get_songs(self, request, pk=None):
        """获取当前歌单的所有歌曲"""
        try:
            playlistId = self.get_object().playlist_id
            raw_songs = PlaylistSong.objects.filter(playlist_id=playlistId).select_related('song')
            # 只返回已审核的歌曲
            songs = [raw_song.song for raw_song in raw_songs if raw_song.song.is_active]
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            return Response({'error': '歌单不存在'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def star(self, request, pk=None):
        """收藏歌单"""
        playlist = self.get_object()
        star_playlist, created = StarPlaylist.objects.get_or_create(
            user=request.user,
            playlist=playlist
        )
        if created:
            return Response({
                'message': '收藏成功',
                'star_playlist': StarPlaylistSerializer(star_playlist).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '已经收藏过该歌单'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unstar(self, request, pk=None):
        """取消收藏"""
        playlist = self.get_object()
        star_playlist = StarPlaylist.objects.filter(user=request.user, playlist=playlist).first()
        if star_playlist:
            star_playlist.delete()
            return Response({'message': '取消收藏成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '未收藏该歌单'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_starred(self, request):
        """获取用户收藏的歌单"""
        starred_playlists = StarPlaylist.objects.filter(
            user=request.user
        ).select_related('playlist').order_by('-star_time')
        
        # 添加分页支持
        page = self.paginate_queryset(starred_playlists)
        if page is not None:
            # 序列化数据
            playlists = [item.playlist for item in page]
            serializer = PlaylistSerializer(playlists, many=True)
            return Response({
                'data': {
                    'playlists': serializer.data,
                    'total': self.paginator.page.paginator.count
                }
            })
        
        playlists = [item.playlist for item in starred_playlists]
        serializer = PlaylistSerializer(playlists, many=True)
        return Response({
            'data': {
                'playlists': serializer.data,
                'total': starred_playlists.count()
            }
        })
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_playlists(self, request):
        """获取当前用户创建的歌单"""
        playlists = Playlist.objects.filter(playlist_creator=request.user)
        # 添加分页支持
        page = self.paginate_queryset(playlists)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'data': {
                    'playlists': serializer.data,
                    'total': self.paginator.page.paginator.count
                }
            })
        serializer = self.get_serializer(playlists, many=True)
        return Response({
            'data': {
                'playlists': serializer.data,
                'total': playlists.count()
            }
        })
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def starred(self, request):
        """获取当前用户收藏的歌单"""
        star_playlists = StarPlaylist.objects.filter(user=request.user).select_related('playlist')
        playlists = [star_playlist.playlist for star_playlist in star_playlists]
        serializer = self.get_serializer(playlists, many=True)
        return Response({
            'data': {
                'playlists': serializer.data,
                'total': len(playlists)
            }
        })
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def check_star(self, request, pk=None):
        """检查用户是否收藏了歌单"""
        # 直接获取歌单对象，不使用get_object()以绕过权限限制
        try:
            playlist = Playlist.objects.get(pk=pk)
            is_starred = StarPlaylist.objects.filter(user=request.user, playlist=playlist).exists()
            return Response({'is_starred': is_starred}, status=status.HTTP_200_OK)
        except Playlist.DoesNotExist:
            return Response({'error': '歌单不存在'}, status=status.HTTP_404_NOT_FOUND)


