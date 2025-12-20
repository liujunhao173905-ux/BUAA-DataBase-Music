"""
用户路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    UserDetailView,
    FollowView,
    FollowersListView,
    FollowingListView,
    MyFollowingListView,
    SingerListView,
    LoginLogViewSet,
)

router = DefaultRouter()
router.register(r'login-logs', LoginLogViewSet, basename='login-log')

urlpatterns = [
    # 认证相关
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # 日志相关
    path('logs/', include(router.urls)),

    # 用户资料
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    
    # 关注相关
    path('<int:user_id>/follow/', FollowView.as_view(), name='follow-user'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
    path('me/following/', MyFollowingListView.as_view(), name='my-following-list'),
    # 歌手列表
    path('singers/', SingerListView.as_view(), name='singer-list'),
]

