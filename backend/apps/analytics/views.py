"""
统计分析视图
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from apps.users.models import LoginLog, User
from apps.music.models import Song, StarSong, BuySong
from apps.playlists.models import Playlist, StarPlaylist


class LoginStatisticsView(APIView):
    """登录统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取登录统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看登录统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 时间范围参数
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # 按用户类型统计
        logs = LoginLog.objects.filter(log_time__gte=start_date)
        stats_by_type = logs.values('log_user_type').annotate(
            count=Count('log_id')
        ).order_by('log_user_type')
        
        # 按日期统计
        stats_by_date = logs.extra(
            select={'date': "DATE(log_time)"}
        ).values('date').annotate(
            count=Count('log_id')
        ).order_by('date')
        
        # 总登录次数
        total_logins = logs.count()
        
        # 活跃用户数（最近N天有登录的用户）
        active_users = User.objects.filter(
            login_logs__log_time__gte=start_date
        ).distinct().count()
        
        return Response({
            'period_days': days,
            'total_logins': total_logins,
            'active_users': active_users,
            'stats_by_type': list(stats_by_type),
            'stats_by_date': list(stats_by_date),
        })


class UserStatisticsView(APIView):
    """用户统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取用户统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看用户统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 按用户类型统计
        stats_by_type = User.objects.values('user_type').annotate(
            count=Count('user_id')
        ).order_by('user_type')
        
        # 总用户数
        total_users = User.objects.count()
        
        # 最近注册的用户数（最近30天）
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        recent_users = User.objects.filter(date_joined__gte=start_date).count()
        
        return Response({
            'total_users': total_users,
            'recent_users': recent_users,
            'stats_by_type': list(stats_by_type),
        })


class MusicStatisticsView(APIView):
    """音乐统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取音乐统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看音乐统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 总歌曲数
        total_songs = Song.objects.count()
        
        # 已上架歌曲数
        active_songs = Song.objects.filter(is_active=True).count()
        
        # 总收藏数
        total_stars = StarSong.objects.count()
        
        # 总购买数
        total_buys = BuySong.objects.count()
        
        # 总销售额
        total_revenue = BuySong.objects.aggregate(
            total=Sum('buy_price')
        )['total'] or 0
        
        # 按歌手统计
        stats_by_singer = Song.objects.values(
            'song_singer__user_name'
        ).annotate(
            song_count=Count('song_id'),
            star_count=Count('starred_by'),
            buy_count=Count('bought_by')
        ).order_by('-song_count')[:10]
        
        return Response({
            'total_songs': total_songs,
            'active_songs': active_songs,
            'total_stars': total_stars,
            'total_buys': total_buys,
            'total_revenue': float(total_revenue),
            'stats_by_singer': list(stats_by_singer),
        })


class PlaylistStatisticsView(APIView):
    """歌单统计视图（管理员端）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取歌单统计"""
        if request.user.user_type != 2:
            return Response(
                {'error': '只有管理员可以查看歌单统计'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 总歌单数
        total_playlists = Playlist.objects.count()
        
        # 公开歌单数
        active_playlists = Playlist.objects.filter(is_active=True).count()
        
        # 总收藏数
        total_stars = StarPlaylist.objects.count()
        
        # 按创建者统计
        stats_by_creator = Playlist.objects.values(
            'playlist_creator__user_name'
        ).annotate(
            playlist_count=Count('playlist_id'),
            star_count=Count('starred_by')
        ).order_by('-playlist_count')[:10]
        
        return Response({
            'total_playlists': total_playlists,
            'active_playlists': active_playlists,
            'total_stars': total_stars,
            'stats_by_creator': list(stats_by_creator),
        })

