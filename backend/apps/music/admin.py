"""
音乐管理后台
"""
from django.contrib import admin
from .models import Song, StarSong, BuySong


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """歌曲管理"""
    list_display = ['song_id', 'song_name', 'song_singer', 'song_price', 'is_active', 'song_createtime']
    list_filter = ['is_active', 'song_createtime', 'song_singer']
    search_fields = ['song_name', 'song_singer__user_name']
    ordering = ['-song_createtime']


@admin.register(StarSong)
class StarSongAdmin(admin.ModelAdmin):
    """收藏歌曲管理"""
    list_display = ['star_song_id', 'user', 'song', 'star_time']
    list_filter = ['star_time']
    search_fields = ['user__user_name', 'song__song_name']


@admin.register(BuySong)
class BuySongAdmin(admin.ModelAdmin):
    """购买歌曲管理"""
    list_display = ['buy_song_id', 'user', 'song', 'buy_price', 'buy_time']
    list_filter = ['buy_time']
    search_fields = ['user__user_name', 'song__song_name']

