"""
审核视图
"""
from rest_framework import status, permissions, viewsets
from rest_framework.permissions import BasePermission
from .pagination import CustomPageNumberPagination
from django.db.models import Q


class IsAdminUser(BasePermission):
    """自定义管理员权限：只有user_type为2的用户才能访问"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 2
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import CheckSongLog, CheckPlaylistLog, CheckUserLog
from .serializers import (
    CheckSongLogSerializer,
    CheckPlaylistLogSerializer,
    CheckUserLogSerializer
)
from apps.music.models import Song
from apps.playlists.models import Playlist
from apps.users.models import User


class CheckSongLogViewSet(viewsets.ModelViewSet):
    """歌曲审核日志视图集"""
    queryset = CheckSongLog.objects.all()
    serializer_class = CheckSongLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        """根据用户类型返回不同的查询集"""
        queryset = CheckSongLog.objects.select_related('check_song', 'check_admin')
        
        # 歌手只能看到自己歌曲的审核记录
        if self.request.user.user_type == 1:
            queryset = queryset.filter(check_song__song_singer=self.request.user)
        # 管理员可以看到所有审核记录
        
        # 按状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None and status_filter.strip() != '':
            try:
                # 支持数组格式的status参数
                status_list = list(map(int, status_filter.split(',')))
                if len(status_list) > 1:
                    queryset = queryset.filter(check_status__in=status_list)
                else:
                    queryset = queryset.filter(check_status=status_list[0])
            except:
                # 如果解析失败，尝试作为单个状态处理
                queryset = queryset.filter(check_status=int(status_filter))
        
        return queryset.order_by('-check_submit_time')
    
    def get_permissions(self):
        """权限控制：只有管理员可以审核"""
        if self.action in ['list', 'retrieve']:
            # 列表和详情：歌手和管理员都可以查看
            return [permissions.IsAuthenticated()]
        else:
            # 审核操作：只有管理员可以
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
    
    def perform_create(self, serializer):
        """创建审核记录（通常由系统自动创建）"""
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        """审核通过"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        if check_log.check_status != 0:
            return Response(
                {'error': '该审核记录已经处理过了'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 更新审核状态
        check_log.check_status = 1  # 审核通过
        check_log.check_admin = request.user
        check_log.check_comment = request.data.get('comment', '')
        check_log.save()
        
        # 更新歌曲状态
        song = check_log.check_song
        song.is_active = True
        song.save()
        
        return Response({
            'message': '审核通过',
            'check_log': CheckSongLogSerializer(check_log).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """审核拒绝"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        if check_log.check_status != 0:
            return Response(
                {'error': '该审核记录已经处理过了'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment = request.data.get('comment', '')
        
        # 更新审核状态
        check_log.check_status = 2  # 审核拒绝
        check_log.check_admin = request.user
        check_log.check_comment = comment
        check_log.save()
        
        # 歌曲保持未上架状态
        song = check_log.check_song
        song.is_active = False
        song.save()
        
        return Response({
            'message': '审核已拒绝',
            'check_log': CheckSongLogSerializer(check_log).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clear(self, request, pk=None):
        """清空审核，重置为待审核状态"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以清空审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        
        # 更新审核状态
        check_log.check_status = 0  # 重置为待审核
        check_log.check_admin = None  # 清空审核管理员
        check_log.check_comment = ''  # 清空审核意见
        check_log.save()
        
        # 歌曲重置为未上架状态
        song = check_log.check_song
        song.is_active = False
        song.save()
        
        return Response({
            'message': '审核已清空',
            'check_log': CheckSongLogSerializer(check_log).data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clear_all(self, request):
        """清空所有已通过或拒绝的审核记录"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以清空审核记录'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 删除所有已通过（1）或拒绝（2）的审核记录
        deleted_count, _ = CheckSongLog.objects.filter(
            check_status__in=[1, 2]
        ).delete()
        
        return Response({
            'message': f'已清空 {deleted_count} 条审核记录',
            'deleted_count': deleted_count
        })


class CheckPlaylistLogViewSet(viewsets.ModelViewSet):
    """歌单审核日志视图集"""
    queryset = CheckPlaylistLog.objects.all()
    serializer_class = CheckPlaylistLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        """根据用户类型返回不同的查询集"""
        queryset = CheckPlaylistLog.objects.select_related('check_playlist', 'check_admin')
        
        # 用户只能看到自己歌单的审核记录
        if self.request.user.user_type in [0, 1]:
            queryset = queryset.filter(check_playlist__playlist_creator=self.request.user)
        
        # 按状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None and status_filter.strip() != '':
            try:
                # 支持数组格式的status参数
                status_list = list(map(int, status_filter.split(',')))
                if len(status_list) > 1:
                    queryset = queryset.filter(check_status__in=status_list)
                else:
                    queryset = queryset.filter(check_status=status_list[0])
            except:
                # 如果解析失败，尝试作为单个状态处理
                queryset = queryset.filter(check_status=int(status_filter))
        
        return queryset.order_by('-check_submit_time')
    
    def get_permissions(self):
        """权限控制"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        """审核通过"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        if check_log.check_status != 0:
            return Response(
                {'error': '该审核记录已经处理过了'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        check_log.check_status = 1
        check_log.check_admin = request.user
        check_log.check_comment = request.data.get('comment', '')
        check_log.save()
        
        playlist = check_log.check_playlist
        playlist.is_active = True
        playlist.save()
        
        return Response({
            'message': '审核通过',
            'check_log': CheckPlaylistLogSerializer(check_log).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """审核拒绝"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        if check_log.check_status != 0:
            return Response(
                {'error': '该审核记录已经处理过了'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment = request.data.get('comment', '')
        
        check_log.check_status = 2
        check_log.check_admin = request.user
        check_log.check_comment = comment
        check_log.save()
        
        playlist = check_log.check_playlist
        playlist.is_active = False
        playlist.save()
        
        return Response({
            'message': '审核已拒绝',
            'check_log': CheckPlaylistLogSerializer(check_log).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clear(self, request, pk=None):
        """清空审核，重置为待审核状态"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以清空审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        
        # 更新审核状态
        check_log.check_status = 0  # 重置为待审核
        check_log.check_admin = None  # 清空审核管理员
        check_log.check_comment = ''  # 清空审核意见
        check_log.save()
        
        # 歌单重置为未上架状态
        playlist = check_log.check_playlist
        playlist.is_active = False
        playlist.save()
        
        return Response({
            'message': '审核已清空',
            'check_log': CheckPlaylistLogSerializer(check_log).data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clear_all(self, request):
        """清空所有已通过或拒绝的审核记录"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以清空审核记录'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 删除所有已通过（1）或拒绝（2）的审核记录
        deleted_count, _ = CheckPlaylistLog.objects.filter(
            check_status__in=[1, 2]
        ).delete()
        
        return Response({
            'message': f'已清空 {deleted_count} 条审核记录',
            'deleted_count': deleted_count
        })


class CheckUserLogViewSet(viewsets.ModelViewSet):
    """用户审核日志视图集"""
    queryset = CheckUserLog.objects.all()
    serializer_class = CheckUserLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        """根据用户类型返回不同的查询集"""
        queryset = CheckUserLog.objects.select_related('check_user', 'check_admin')
        
        # 用户只能看到自己的审核记录
        if self.request.user.user_type in [0, 1]:
            queryset = queryset.filter(check_user=self.request.user)
        
        # 按状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None and status_filter.strip() != '':
            try:
                # 支持数组格式的status参数
                status_list = list(map(int, status_filter.split(',')))
                if len(status_list) > 1:
                    queryset = queryset.filter(check_status__in=status_list)
                else:
                    queryset = queryset.filter(check_status=status_list[0])
            except:
                # 如果解析失败，尝试作为单个状态处理
                queryset = queryset.filter(check_status=int(status_filter))
        
        return queryset.order_by('-check_submit_time')
    
    def get_permissions(self):
        """权限控制"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        """审核通过"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        if check_log.check_status != 0:
            return Response(
                {'error': '该审核记录已经处理过了'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        check_log.check_status = 1
        check_log.check_admin = request.user
        check_log.check_comment = request.data.get('comment', '')
        check_log.save()
        
        # 用户审核通过后，将普通用户改为歌手
        user = check_log.check_user
        if user.user_type == 0 and check_log.check_user_type == 1:
            user.user_type = 1  # 改为歌手类型
            user.save()
            
        # 这里可以添加其他业务逻辑，比如发送通知等
        
        return Response({
            'message': '审核通过',
            'check_log': CheckUserLogSerializer(check_log).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """审核拒绝"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        if check_log.check_status != 0:
            return Response(
                {'error': '该审核记录已经处理过了'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment = request.data.get('comment', '')
        
        check_log.check_status = 2
        check_log.check_admin = request.user
        check_log.check_comment = comment
        check_log.save()
        
        # 审核拒绝后，可以将用户类型改回普通用户
        user = check_log.check_user
        if user.user_type == 1:
            user.user_type = 0
            user.save()
        
        return Response({
            'message': '审核已拒绝',
            'check_log': CheckUserLogSerializer(check_log).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clear(self, request, pk=None):
        """清空审核，重置为待审核状态"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以清空审核'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        check_log = self.get_object()
        
        # 更新审核状态
        check_log.check_status = 0  # 重置为待审核
        check_log.check_admin = None  # 清空审核管理员
        check_log.check_comment = ''  # 清空审核意见
        check_log.save()
        
        # 用户重置为普通用户类型
        user = check_log.check_user
        if user.user_type != 0:
            user.user_type = 0
            user.save()
        
        return Response({
            'message': '审核已清空',
            'check_log': CheckUserLogSerializer(check_log).data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clear_all(self, request):
        """清空所有已通过或拒绝的审核记录"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以清空审核记录'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 删除所有已通过（1）或拒绝（2）的审核记录
        deleted_count, _ = CheckUserLog.objects.filter(
            check_status__in=[1, 2]
        ).delete()
        
        return Response({
            'message': f'已清空 {deleted_count} 条审核记录',
            'deleted_count': deleted_count
        })

