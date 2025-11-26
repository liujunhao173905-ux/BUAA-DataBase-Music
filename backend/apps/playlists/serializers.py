"""
歌单序列化器
"""
from rest_framework import serializers
from .models import Playlist, PlaylistSong, StarPlaylist
from apps.music.serializers import SongSerializer


class PlaylistSongSerializer(serializers.ModelSerializer):
    """歌单歌曲序列化器"""
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = PlaylistSong
        fields = ['playlist_songs_id', 'playlist', 'song', 'add_time', 'order']
        read_only_fields = ['playlist_songs_id', 'add_time']


class PlaylistSerializer(serializers.ModelSerializer):
    """歌单序列化器"""
    playlist_creator_name = serializers.CharField(source='playlist_creator.user_name', read_only=True)
    playlist_creator_id = serializers.IntegerField(source='playlist_creator.user_id', read_only=True)
    song_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    star_count = serializers.SerializerMethodField()
    songs = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = [
            'playlist_id', 'playlist_name', 'playlist_cover', 'playlist_intro',
            'playlist_creator', 'playlist_creator_name', 'playlist_creator_id',
            'playlist_createtime', 'playlist_updatetime', 'is_active',
            'song_count', 'is_starred', 'star_count', 'songs'
        ]
        read_only_fields = ['playlist_id', 'playlist_createtime', 'playlist_updatetime']
    
    def get_song_count(self, obj):
        """获取歌曲数量"""
        return obj.songs.count()
    
    def get_is_starred(self, obj):
        """检查当前用户是否已收藏"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return StarPlaylist.objects.filter(user=request.user, playlist=obj).exists()
        return False
    
    def get_star_count(self, obj):
        """获取收藏数"""
        return obj.starred_by.count()
    
    def get_songs(self, obj):
        """获取歌单中的歌曲列表"""
        playlist_songs = obj.songs.all().select_related('song')
        return PlaylistSongSerializer(playlist_songs, many=True, context=self.context).data


class PlaylistCreateSerializer(serializers.ModelSerializer):
    """歌单创建序列化器"""
    
    class Meta:
        model = Playlist
        fields = ['playlist_name', 'playlist_cover', 'playlist_intro']
    
    def create(self, validated_data):
        """创建歌单，自动设置为当前用户"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('需要登录')
        
        validated_data['playlist_creator'] = request.user
        validated_data['is_active'] = False  # 新创建的歌单需要审核
        playlist = Playlist.objects.create(**validated_data)
        return playlist


class StarPlaylistSerializer(serializers.ModelSerializer):
    """收藏歌单序列化器"""
    playlist = PlaylistSerializer(read_only=True)
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    
    class Meta:
        model = StarPlaylist
        fields = ['star_playlist_id', 'user', 'user_name', 'playlist', 'star_time']
        read_only_fields = ['star_playlist_id', 'star_time']

