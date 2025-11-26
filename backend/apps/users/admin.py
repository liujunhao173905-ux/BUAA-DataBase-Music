"""
用户管理后台
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Follow, LoginLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ['user_id', 'user_name', 'user_mobile', 'user_type', 'is_active', 'user_createtime']
    list_filter = ['user_type', 'is_active', 'user_createtime']
    search_fields = ['user_name', 'user_mobile']
    ordering = ['-user_createtime']
    filter_horizontal = []
    
    fieldsets = (
        (None, {'fields': ('user_name', 'password')}),
        ('个人信息', {'fields': ('user_mobile', 'user_avatar', 'user_type')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('时间', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'password1', 'password2', 'user_type'),
        }),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """关注关系管理"""
    list_display = ['follow_id', 'follower', 'following', 'follow_time']
    list_filter = ['follow_time']
    search_fields = ['follower__user_name', 'following__user_name']


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """登录日志管理"""
    list_display = ['log_id', 'log_user_name', 'log_user_type', 'log_time']
    list_filter = ['log_user_type', 'log_time']
    search_fields = ['log_user_name']
    readonly_fields = ['log_id', 'log_time']
    ordering = ['-log_time']

