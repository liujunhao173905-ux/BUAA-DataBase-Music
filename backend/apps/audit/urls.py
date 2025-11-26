"""
审核路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckSongLogViewSet, CheckPlaylistLogViewSet, CheckUserLogViewSet

router = DefaultRouter()
router.register(r'songs', CheckSongLogViewSet, basename='check-song')
router.register(r'playlists', CheckPlaylistLogViewSet, basename='check-playlist')
router.register(r'users', CheckUserLogViewSet, basename='check-user')

urlpatterns = [
    path('', include(router.urls)),
]

