"""
音乐路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, SongStatisticsView

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')

urlpatterns = [
    path('', include(router.urls)),
    path('songs/<int:song_id>/statistics/', SongStatisticsView.as_view(), name='song-statistics'),
    path('songs/statistics/', SongStatisticsView.as_view(), name='songs-statistics'),
]

