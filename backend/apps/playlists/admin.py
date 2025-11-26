"""
歌单管理后台
"""
from django.contrib import admin
from .models import Playlist, PlaylistSong, StarPlaylist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """歌单管理"""
    list_display = ['playlist_id', 'playlist_name', 'playlist_creator', 'is_active', 'playlist_createtime']
    list_filter = ['is_active', 'playlist_createtime']
    search_fields = ['playlist_name', 'playlist_creator__user_name']


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    """歌单歌曲管理"""
    list_display = ['playlist_songs_id', 'playlist', 'song', 'order', 'add_time']
    list_filter = ['add_time']
    search_fields = ['playlist__playlist_name', 'song__song_name']


@admin.register(StarPlaylist)
class StarPlaylistAdmin(admin.ModelAdmin):
    """收藏歌单管理"""
    list_display = ['star_playlist_id', 'user', 'playlist', 'star_time']
    list_filter = ['star_time']
    search_fields = ['user__user_name', 'playlist__playlist_name']

