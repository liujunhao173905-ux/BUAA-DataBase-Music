"""
音乐视图
"""
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count
from django.utils import timezone
from .models import Song, StarSong, BuySong, PlayHistory
from .serializers import SongSerializer, SongCreateSerializer, SongUpdateSerializer, StarSongSerializer, BuySongSerializer
from apps.users.models import LoginLog
from apps.audit.models import CheckSongLog
import openpyxl
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from io import BytesIO


class SongExportView(APIView):
    """歌曲导出视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 使用 export_type 替代 format，避免 DRF 内容协商冲突
        format_type = request.query_params.get('export_type', 'excel')
        # 兼容旧代码
        if not request.query_params.get('export_type') and request.query_params.get('format'):
            format_type = request.query_params.get('format')
            
        song_ids = request.query_params.get('song_ids') # 逗号分隔的ID字符串
        
        # 筛选逻辑：歌手只能导出自己的，管理员导出所有，普通用户不能导出
        if request.user.user_type == 1: # 歌手
            songs = Song.objects.filter(song_singer=request.user)
        elif request.user.user_type == 2: # 管理员
            songs = Song.objects.all()
        else:
            return Response({'error': '无权操作'}, status=status.HTTP_403_FORBIDDEN)
            
        # 如果指定了ID，进一步筛选
        if song_ids:
            try:
                id_list = [int(id_str) for id_str in song_ids.split(',') if id_str.strip()]
                songs = songs.filter(song_id__in=id_list)
            except ValueError:
                return Response({'error': '无效的歌曲ID格式'}, status=status.HTTP_400_BAD_REQUEST)
            
        if format_type == 'xml':
            return self._export_xml(songs)
        else:
            return self._export_excel(songs)

    def _export_excel(self, songs):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "歌曲列表"
        
        headers = ['歌曲ID', '歌曲名', '歌手', '时长(秒)', '价格', '上架状态', '创建时间']
        ws.append(headers)

        status_map = {0: '审核中', 1: '已上架', 2: '未过审', 3: '已锁定'}
        
        for song in songs:
            ws.append([
                song.song_id,
                song.song_name,
                song.song_singer.user_name,
                song.song_duration,
                song.song_price,
                status_map.get(song.song_status, '未知'),
                song.song_createtime.strftime('%Y-%m-%d %H:%M:%S')
            ])
            
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="songs_export_{timezone.now().strftime("%Y%m%d")}.xlsx"'
        return response

    def _export_xml(self, songs):
        root = ET.Element("songs")

        status_map = {0: '审核中', 1: '已上架', 2: '未过审', 3: '已锁定'}
        
        for song in songs:
            song_elem = ET.SubElement(root, "song")
            ET.SubElement(song_elem, "id").text = str(song.song_id)
            ET.SubElement(song_elem, "name").text = song.song_name
            ET.SubElement(song_elem, "singer").text = song.song_singer.user_name
            ET.SubElement(song_elem, "duration").text = str(song.song_duration)
            ET.SubElement(song_elem, "price").text = str(song.song_price)
            ET.SubElement(song_elem, "status").text = status_map.get(song.song_status, '未知')
            ET.SubElement(song_elem, "create_time").text = song.song_createtime.strftime('%Y-%m-%d %H:%M:%S')
            
        xml_str = ET.tostring(root, encoding='utf-8', method='xml')
        
        response = HttpResponse(xml_str, content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename="songs_export_{timezone.now().strftime("%Y%m%d")}.xml"'
        return response


class SongImportView(APIView):
    """歌曲导入视图"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.user_type not in [1, 2]:
            return Response({'error': '无权操作'}, status=status.HTTP_403_FORBIDDEN)
            
        file = request.FILES.get('file')
        if not file:
            return Response({'error': '请上传文件'}, status=status.HTTP_400_BAD_REQUEST)
            
        if file.name.endswith('.xlsx'):
            return self._import_excel(file, request.user)
        elif file.name.endswith('.xml'):
            return self._import_xml(file, request.user)
        else:
            return Response({'error': '不支持的文件格式'}, status=status.HTTP_400_BAD_REQUEST)

    def _import_excel(self, file, user):
        try:
            wb = openpyxl.load_workbook(file)
            ws = wb.active
            
            success_count = 0
            errors = []
            
            # 跳过表头，从第二行开始
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
                try:
                    # 假设列顺序: Name, Singer, Duration, Price, Status, CreateTime
                    # 我们主要导入 Name, Duration, Price
                    
                    song_name = row[0]
                    duration = row[2]
                    price = row[3]
                    
                
                        # 创建新歌曲
                    if user.user_type == 1:
                        Song.objects.create(
                            song_name=song_name,
                            song_singer=user,
                            song_duration=int(duration) if duration else 0,
                            song_price=float(price) if price else 0,
                            song_status=0,
                            song_file='songs/placeholder.mp3' # 占位文件
                        )
                        success_count += 1
                    else:
                        errors.append(f"第{row_idx}行: 只有歌手可以创建歌曲")    
                        
                except Exception as e:
                    errors.append(f"第{row_idx}行: 处理失败 - {str(e)}")
            
            return Response({
                'message': f'导入完成，成功 {success_count} 条',
                'errors': errors
            })
            
        except Exception as e:
            return Response({'error': f'Excel解析失败: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    def _import_xml(self, file, user):
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            
            success_count = 0
            errors = []
            
            for idx, song_elem in enumerate(root.findall('song'), 1):
                try:
                    song_id_elem = song_elem.find('id')
                    name_elem = song_elem.find('name')
                    duration_elem = song_elem.find('duration')
                    price_elem = song_elem.find('price')
                    
                    if song_id_elem is not None and song_id_elem.text:
                        song_id = int(song_id_elem.text)
                        song = Song.objects.filter(song_id=song_id).first()
                        
                        if song:
                            if user.user_type == 1 and song.song_singer != user:
                                errors.append(f"第{idx}个歌曲: 无权修改其他歌手的歌曲")
                                continue
                                
                            if name_elem is not None: song.song_name = name_elem.text
                            if duration_elem is not None: song.song_duration = int(duration_elem.text)
                            if price_elem is not None: song.song_price = float(price_elem.text)
                            song.save()
                            success_count += 1
                        else:
                            errors.append(f"第{idx}个歌曲: ID不存在")
                    else:
                        # 创建新歌曲
                        if user.user_type == 1:
                            name = name_elem.text if name_elem is not None else "Unknown"
                            duration = int(duration_elem.text) if duration_elem is not None and duration_elem.text else 0
                            price = float(price_elem.text) if price_elem is not None and price_elem.text else 0
                            
                            Song.objects.create(
                                song_name=name,
                                song_singer=user,
                                song_duration=duration,
                                song_price=price,
                                song_status=0,
                                song_file='songs/placeholder.mp3'
                            )
                            success_count += 1
                        else:
                            errors.append(f"第{idx}个歌曲: 只有歌手可以创建歌曲")
                        
                except Exception as e:
                    errors.append(f"第{idx}个歌曲: 处理失败 - {str(e)}")
            
            return Response({
                'message': f'导入完成，成功 {success_count} 条',
                'errors': errors
            })
            
        except Exception as e:
            return Response({'error': f'XML解析失败: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class ExternalMusicSearchView(APIView):
    """外部音乐搜索视图（模拟）"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response([])
            
        # 模拟外部API数据
        # 在实际项目中，这里会调用 Spotify/Apple Music/Netease API
        mock_results = [
            {
                'external_id': f'ext_{i}',
                'name': f'{keyword} - Version {i}',
                'singer': f'External Artist {i}',
                'duration': 180 + i * 10,
                'cover': 'https://via.placeholder.com/150',
                'price': 0.00
            }
            for i in range(1, 6)
        ]
        
        return Response(mock_results)


class ExternalMusicImportView(APIView):
    """外部音乐导入视图"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.user_type != 1: # 仅歌手可导入
            return Response({'error': '只有歌手可以导入歌曲'}, status=status.HTTP_403_FORBIDDEN)
            
        external_data = request.data
        name = external_data.get('name')
        duration = external_data.get('duration', 0)
        
        if not name:
            return Response({'error': '歌曲信息不完整'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 创建新歌曲
        # 注意：这里我们没有实际的音频文件，所以创建一个占位符或需要后续上传
        # 为了演示，我们假设这是一个元数据导入
        try:
            song = Song.objects.create(
                song_name=name,
                song_singer=request.user,
                song_duration=duration,
                song_price=0.00,
                song_status=0, # 导入后默认为未上架，需审核或上传文件
                # song_file 需要一个默认值，或者允许为空（如果模型允许）
                # 由于模型FileField默认必须有值，这里我们可能需要一个默认文件，或者修改模型
                # 暂时先用一个空字符串或占位路径，这可能会导致文件操作错误，但仅做演示
                song_file='songs/placeholder.mp3' 
            )
            return Response({'message': '导入成功', 'song_id': song.song_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'导入失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecordPlayView(APIView):
    """记录播放历史"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        song_id = request.data.get('song_id')
        duration = request.data.get('duration', 0)
        
        if not song_id:
            return Response({'error': '缺少歌曲ID'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            song = Song.objects.get(song_id=song_id)
            PlayHistory.objects.create(
                user=request.user,
                song=song,
                play_duration=duration
            )
            return Response({'message': '记录成功'}, status=status.HTTP_201_CREATED)
        except Song.DoesNotExist:
            return Response({'error': '歌曲不存在'}, status=status.HTTP_404_NOT_FOUND)


class SongViewSet(viewsets.ModelViewSet):
    """歌曲视图集"""
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_field = 'pk'
    
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
            queryset = queryset.filter(song_status=1)
        # 歌手可以看到自己的所有歌曲
        elif self.request.user.user_type == 1:
            queryset = queryset.filter(
                Q(song_status=1) | Q(song_singer=self.request.user)
            )
        # 管理员可以看到所有歌曲
        
        return queryset.order_by('-song_createtime')
    
    def get_serializer_class(self):
        """根据操作选择不同的序列化器"""
        if self.action == 'create':
            return SongCreateSerializer
        elif self.action == 'update':
            return SongUpdateSerializer
        return SongSerializer
    
    def get_serializer_context(self):
        """将请求对象添加到序列化器上下文中"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_permissions(self):
        """权限控制"""
        if self.action in ['list', 'retrieve', 'recommend']:
            # 列表、详情和推荐允许所有用户访问
            return [permissions.AllowAny()]
        elif self.action == 'create':
            # 创建需要歌手权限
            return [permissions.IsAuthenticated()]
        else:
            # 更新和删除需要歌手权限（只能操作自己的歌曲）或管理员权限
            return [permissions.IsAuthenticated()]
    
    def get_object(self):
        """获取单个对象，确保歌手可以删除自己的任何歌曲"""
        # 对于删除操作，绕过get_queryset的过滤，确保能找到自己的歌曲
        if self.action == 'destroy':
            try:
                song_id = self.kwargs.get('song_id') or self.kwargs.get('pk')
                if self.request.user.user_type == 2:
                    # 管理员可以获取任何歌曲
                    return Song.objects.get(song_id=song_id)
                else:
                    # 普通用户只能获取自己的歌曲
                    return Song.objects.get(song_id=song_id, song_singer=self.request.user)
            except Song.DoesNotExist:
                from rest_framework.exceptions import NotFound
                raise NotFound(detail='歌曲不存在或无权访问')
        
        # 其他操作使用默认的get_object方法
        return super().get_object()
    
    def perform_create(self, serializer):
        """创建歌曲"""
        serializer.save()
    
    def perform_update(self, serializer):
        """更新歌曲（需要重新审核）"""
        song = serializer.save()
        song.song_status = 0  # 修改后需要重新审核
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
        # if song.song_price == 0:
        #     return Response({'error': '该歌曲是免费的，无需购买'}, status=status.HTTP_400_BAD_REQUEST)
        
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
    def starred(self, request):
        """获取当前用户收藏的歌曲"""
        # 获取用户收藏的歌曲，按收藏时间倒序
        star_songs = StarSong.objects.filter(user=request.user)\
            .select_related('song', 'song__song_singer')\
            .order_by('-star_time')
        
        # 支持分页
        page = self.paginate_queryset(star_songs)
        if page is not None:
            songs = [item.song for item in page]
            serializer = self.get_serializer(songs, many=True)
            return self.get_paginated_response(serializer.data)
            
        songs = [item.song for item in star_songs]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def bought(self, request):
        """获取当前用户购买的歌曲"""
        # 1. 当前用户的购买记录，按最新排序
        buy_qs = BuySong.objects.filter(user=request.user) \
            .select_related('song') \
            .order_by('-buy_song_id')

        # 2. 构造  song_id -> buy_price  映射
        buy_map: dict[int, str] = {
            buy.song_id: str(buy.buy_price) for buy in buy_qs
        }

        # 3. 只取歌曲实例（去重，保留最新一条即可）
        songs = [buy.song for buy in buy_qs if buy.song.song_status == 1]

        # 4. 分页
        page = self.paginate_queryset(songs)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'buy_map': buy_map})
            print(serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(songs, many=True, context={'buy_map': buy_map})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def recommend(self, request):

        """推荐歌曲（按收藏量排序）"""
        songs = Song.objects.filter(song_status=1).annotate(
            star_count=Count('starred_by')
        ).order_by('-star_count')[:10]
        
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_songs(self, request):
        """获取当前歌手上传的歌曲"""
        if request.user.user_type != 1:
            return Response(
                {'error': '只有歌手可以查看自己的歌曲'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        songs = Song.objects.filter(song_singer=request.user)
        # 添加分页支持
        page = self.paginate_queryset(songs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
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



