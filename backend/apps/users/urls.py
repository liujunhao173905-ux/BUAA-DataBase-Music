"""
用户路由配置
"""
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    UserDetailView,
    FollowView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    # 认证相关
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # 用户资料
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    
    # 关注相关
    path('<int:user_id>/follow/', FollowView.as_view(), name='follow-user'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
]

