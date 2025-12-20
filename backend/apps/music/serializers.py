"""
音乐序列化器
"""
from rest_framework import serializers
from .models import Song, StarSong, BuySong
from apps.users.serializers import UserProfileSerializer
from apps.audit.models import CheckSongLog


class SongSerializer(serializers.ModelSerializer):
    """歌曲序列化器"""
    song_singer_name = serializers.CharField(source='song_singer.user_name', read_only=True)
    song_singer_id = serializers.IntegerField(source='song_singer.user_id', read_only=True)
    is_starred = serializers.SerializerMethodField()
    is_bought = serializers.SerializerMethodField()
    star_count = serializers.SerializerMethodField()
    buy_count = serializers.SerializerMethodField()
    song_price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, read_only=True)
    song_createtime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    song_updatetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    bought_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = [
            'song_id', 'song_name', 'song_cover', 'song_file',
            'song_duration', 'song_price', 'song_singer_name',
            'song_singer_id', 'song_createtime', 'song_updatetime',
            'is_active', 'is_starred', 'is_bought', 'star_count', 'buy_count', 'bought_price'
        ]
        read_only_fields = ['song_id', 'song_createtime', 'song_updatetime']
    
    def get_is_starred(self, obj):
        """检查当前用户是否已收藏"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return StarSong.objects.filter(user=request.user, song=obj).exists()
        return False
    
    def get_is_bought(self, obj):
        """检查当前用户是否已购买"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BuySong.objects.filter(user=request.user, song=obj).exists()
        return False
    
    def get_star_count(self, obj):
        """获取收藏数"""
        return obj.starred_by.count()
    
    def get_buy_count(self, obj):
        """获取购买数"""
        print('debug1')
        return obj.bought_by.count()
    
    def get_bought_price(self, obj):
        print('debug2')
        buy_map = self.context.get('buy_map', {})
        return buy_map.get(obj.song_id, None)

class SongCreateSerializer(serializers.ModelSerializer):
    """歌曲创建序列化器（用于上传）"""
    
    class Meta:
        model = Song
        fields = [
            'song_name', 'song_cover', 'song_file',
            'song_duration', 'song_price'
        ]
    
    def create(self, validated_data):
        """创建歌曲，自动设置为当前登录的歌手"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('需要登录')
        
        if request.user.user_type != 1:
            raise serializers.ValidationError('只有歌手可以上传歌曲')
        
        validated_data['song_singer'] = request.user
        validated_data['is_active'] = False  # 新上传的歌曲需要审核
        song = Song.objects.create(**validated_data)
        
        return song


class SongUpdateSerializer(serializers.ModelSerializer):
    """歌曲更新序列化器（用于上传）"""
    """歌曲封面，不传不修改，传 null 清空"""
    song_cover = serializers.ImageField(required=False, allow_null=True)
    song_file = serializers.FileField(required=False)
    song_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0)
    
    class Meta:
        model = Song
        fields = [
            'song_name', 'song_cover', 'song_file',
            'song_duration', 'song_price'
        ]
    
    def update(self, instance, validated_data):
        """更新歌曲，自动设置为当前登录的歌手"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('需要登录')
        
        if request.user.user_type != 1:
            raise serializers.ValidationError('只有歌手可以更新歌曲')
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        validated_data['is_active'] = False  # 需要重新审核

        instance.save()
        return instance


class StarSongSerializer(serializers.ModelSerializer):
    """收藏歌曲序列化器"""
    song = SongSerializer(read_only=True)
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    star_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = StarSong
        fields = ['star_song_id', 'user', 'user_name', 'song', 'star_time']
        read_only_fields = ['star_song_id', 'star_time']


class BuySongSerializer(serializers.ModelSerializer):
    """购买歌曲序列化器"""
    song = SongSerializer(read_only=True)
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    buy_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = BuySong
        fields = ['buy_song_id', 'user', 'user_name', 'song', 'buy_time', 'buy_price']
        read_only_fields = ['buy_song_id', 'buy_time']

