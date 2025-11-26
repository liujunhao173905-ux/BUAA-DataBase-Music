"""
审核序列化器
"""
from rest_framework import serializers
from .models import CheckSongLog, CheckPlaylistLog, CheckUserLog
from apps.music.serializers import SongSerializer
from apps.playlists.serializers import PlaylistSerializer
from apps.users.serializers import UserProfileSerializer


class CheckSongLogSerializer(serializers.ModelSerializer):
    """歌曲审核日志序列化器"""
    check_song_detail = SongSerializer(source='check_song', read_only=True)
    check_admin_name = serializers.CharField(source='check_admin.user_name', read_only=True)
    check_status_display = serializers.CharField(source='get_check_status_display', read_only=True)
    
    class Meta:
        model = CheckSongLog
        fields = [
            'check_id', 'check_song', 'check_song_detail',
            'check_song_name', 'check_song_cover', 'check_song_file',
            'check_song_duration', 'check_song_price',
            'check_submit_time', 'check_modify_time', 'check_status',
            'check_status_display', 'check_admin', 'check_admin_name', 'check_comment'
        ]
        read_only_fields = ['check_id', 'check_submit_time', 'check_modify_time']


class CheckPlaylistLogSerializer(serializers.ModelSerializer):
    """歌单审核日志序列化器"""
    check_playlist_detail = PlaylistSerializer(source='check_playlist', read_only=True)
    check_admin_name = serializers.CharField(source='check_admin.user_name', read_only=True)
    check_status_display = serializers.CharField(source='get_check_status_display', read_only=True)
    
    class Meta:
        model = CheckPlaylistLog
        fields = [
            'check_id', 'check_playlist', 'check_playlist_detail',
            'check_playlist_name', 'check_playlist_cover', 'check_playlist_intro',
            'check_submit_time', 'check_modify_time', 'check_status',
            'check_status_display', 'check_admin', 'check_admin_name', 'check_comment'
        ]
        read_only_fields = ['check_id', 'check_submit_time', 'check_modify_time']


class CheckUserLogSerializer(serializers.ModelSerializer):
    """用户审核日志序列化器"""
    check_user_detail = UserProfileSerializer(source='check_user', read_only=True)
    check_admin_name = serializers.CharField(source='check_admin.user_name', read_only=True)
    check_status_display = serializers.CharField(source='get_check_status_display', read_only=True)
    
    class Meta:
        model = CheckUserLog
        fields = [
            'check_id', 'check_user', 'check_user_detail',
            'check_user_name', 'check_user_mobile', 'check_user_avatar',
            'check_user_type', 'check_submit_time', 'check_modify_time',
            'check_status', 'check_status_display', 'check_admin',
            'check_admin_name', 'check_comment'
        ]
        read_only_fields = ['check_id', 'check_submit_time', 'check_modify_time']

