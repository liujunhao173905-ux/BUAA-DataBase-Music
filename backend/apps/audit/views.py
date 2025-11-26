"""
审核视图
"""
from rest_framework import status, permissions, viewsets
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
    
    def get_queryset(self):
        """根据用户类型返回不同的查询集"""
        queryset = CheckSongLog.objects.select_related('check_song', 'check_admin')
        
        # 歌手只能看到自己歌曲的审核记录
        if self.request.user.user_type == 1:
            queryset = queryset.filter(check_song__song_singer=self.request.user)
        # 管理员可以看到所有审核记录
        
        # 按状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None:
            queryset = queryset.filter(check_status=int(status_filter))
        
        return queryset.order_by('-check_submit_time')
    
    def get_permissions(self):
        """权限控制：只有管理员可以审核"""
        if self.action in ['list', 'retrieve']:
            # 列表和详情：歌手和管理员都可以查看
            return [permissions.IsAuthenticated()]
        else:
            # 审核操作：只有管理员可以
            return [permissions.IsAuthenticated()]
    
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
        if not comment:
            return Response(
                {'error': '拒绝审核必须提供审核意见'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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


class CheckPlaylistLogViewSet(viewsets.ModelViewSet):
    """歌单审核日志视图集"""
    queryset = CheckPlaylistLog.objects.all()
    serializer_class = CheckPlaylistLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """根据用户类型返回不同的查询集"""
        queryset = CheckPlaylistLog.objects.select_related('check_playlist', 'check_admin')
        
        # 用户只能看到自己歌单的审核记录
        if self.request.user.user_type in [0, 1]:
            queryset = queryset.filter(check_playlist__playlist_creator=self.request.user)
        
        # 按状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None:
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
        if not comment:
            return Response(
                {'error': '拒绝审核必须提供审核意见'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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


class CheckUserLogViewSet(viewsets.ModelViewSet):
    """用户审核日志视图集"""
    queryset = CheckUserLog.objects.all()
    serializer_class = CheckUserLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """根据用户类型返回不同的查询集"""
        queryset = CheckUserLog.objects.select_related('check_user', 'check_admin')
        
        # 用户只能看到自己的审核记录
        if self.request.user.user_type in [0, 1]:
            queryset = queryset.filter(check_user=self.request.user)
        
        # 按状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter is not None:
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
        
        # 用户审核通过后，用户类型保持不变（已经是歌手类型）
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
        if not comment:
            return Response(
                {'error': '拒绝审核必须提供审核意见'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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

