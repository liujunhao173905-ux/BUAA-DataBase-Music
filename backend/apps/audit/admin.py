"""
审核管理后台
"""
from django.contrib import admin
from .models import CheckSongLog, CheckPlaylistLog, CheckUserLog


@admin.register(CheckSongLog)
class CheckSongLogAdmin(admin.ModelAdmin):
    """歌曲审核日志管理"""
    list_display = ['check_id', 'check_song_name', 'check_status', 'check_admin', 'check_submit_time']
    list_filter = ['check_status', 'check_submit_time']
    search_fields = ['check_song_name']


@admin.register(CheckPlaylistLog)
class CheckPlaylistLogAdmin(admin.ModelAdmin):
    """歌单审核日志管理"""
    list_display = ['check_id', 'check_playlist_name', 'check_status', 'check_admin', 'check_submit_time']
    list_filter = ['check_status', 'check_submit_time']
    search_fields = ['check_playlist_name']


@admin.register(CheckUserLog)
class CheckUserLogAdmin(admin.ModelAdmin):
    """用户审核日志管理"""
    list_display = ['check_id', 'check_user_name', 'check_user_type', 'check_status', 'check_admin', 'check_submit_time']
    list_filter = ['check_status', 'check_user_type', 'check_submit_time']
    search_fields = ['check_user_name']

