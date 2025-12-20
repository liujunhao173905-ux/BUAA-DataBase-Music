"""
音乐路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SongViewSet, SongStatisticsView, RecordPlayView, 
    SongExportView, SongImportView,
    ExternalMusicSearchView, ExternalMusicImportView
)

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')

urlpatterns = [
    path('', include(router.urls)),
    path('songs/<int:song_id>/statistics/', SongStatisticsView.as_view(), name='song-statistics'),
    path('songs/statistics/', SongStatisticsView.as_view(), name='songs-statistics'),
    path('record-play/', RecordPlayView.as_view(), name='record-play'),
    path('export/', SongExportView.as_view(), name='song-export'),
    path('import/', SongImportView.as_view(), name='song-import'),
    path('external/search/', ExternalMusicSearchView.as_view(), name='external-music-search'),
    path('external/import/', ExternalMusicImportView.as_view(), name='external-music-import'),
]

