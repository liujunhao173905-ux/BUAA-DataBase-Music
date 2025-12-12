"""
歌单路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaylistViewSet

router = DefaultRouter()
router.register(r'', PlaylistViewSet, basename='playlist')

# 获取自动生成的路由，确认check-star路由是否存在
urlpatterns = [
    path('', include(router.urls)),
    # 显式添加check-star路由以确保它能被正确访问
    path('<int:pk>/check-star/', PlaylistViewSet.as_view({'get': 'check_star'}), name='playlist-check-star'),
]

