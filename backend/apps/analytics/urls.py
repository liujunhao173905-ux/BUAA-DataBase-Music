"""
统计分析路由配置
"""
from django.urls import path
from .views import (
    LoginStatisticsView,
    UserStatisticsView,
    MusicStatisticsView,
    PlaylistStatisticsView,
    UserReportView,
    ExportReportView,
)

urlpatterns = [
    path('login/', LoginStatisticsView.as_view(), name='login-statistics'),
    path('users/', UserStatisticsView.as_view(), name='user-statistics'),
    path('music/', MusicStatisticsView.as_view(), name='music-statistics'),
    path('playlists/', PlaylistStatisticsView.as_view(), name='playlist-statistics'),
    path('report/export/', ExportReportView.as_view(), name='export-user-report'),
    path('user-report/', UserReportView.as_view(), name='user-report'),
]
