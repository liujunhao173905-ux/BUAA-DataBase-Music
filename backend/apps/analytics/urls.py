"""
统计分析路由配置
"""
from django.urls import path
from .views import (
    LoginStatisticsView,
    UserStatisticsView,
    MusicStatisticsView,
    PlaylistStatisticsView,
)

urlpatterns = [
    path('login/', LoginStatisticsView.as_view(), name='login-statistics'),
    path('users/', UserStatisticsView.as_view(), name='user-statistics'),
    path('music/', MusicStatisticsView.as_view(), name='music-statistics'),
    path('playlists/', PlaylistStatisticsView.as_view(), name='playlist-statistics'),
]
