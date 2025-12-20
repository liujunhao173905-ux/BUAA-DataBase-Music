"""
用户序列化器
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Follow, LoginLog


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    password = serializers.CharField(write_only=True, required=False)
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    user_avatar = serializers.ImageField(use_url=True, required=False)
    user_createtime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user_age = serializers.IntegerField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'user_name', 'user_mobile', 'user_avatar',
            'user_gender', 'user_birth_date', 'user_age', 'user_balance',
            'user_createtime', 'user_type', 'user_type_display',
            'is_active', 'password', 'date_joined'
        ]
        read_only_fields = ['user_id', 'user_createtime', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
    
    def validate_password(self, value):
        """验证密码强度"""
        if value:
            validate_password(value)
        return value
    
    def create(self, validated_data):
        """创建用户"""
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """更新用户"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    user_mobile = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = User
        fields = ['user_name', 'user_mobile', 'password', 'password_confirm', 'user_type']
    
    def validate(self, attrs):
        """验证密码确认以及密码强度"""
        password = attrs.get('password')
        if password != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        if password and len(password) < 6:
            raise serializers.ValidationError({"password": "密码长度至少为6位"})
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器（用于显示）"""
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    user_avatar = serializers.ImageField(use_url=True)
    user_createtime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user_age = serializers.IntegerField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'user_name', 'user_mobile', 'user_avatar',
            'user_gender', 'user_birth_date', 'user_age', 'user_balance',
            'user_createtime', 'user_type', 'user_type_display',
            'date_joined', 'followers_count', 'following_count'
        ]
        read_only_fields = ['user_id', 'user_createtime', 'date_joined']
    
    def get_followers_count(self, obj):
        """获取粉丝数"""
        return obj.followers_set.count()
    
    def get_following_count(self, obj):
        """获取关注数"""
        return obj.following_set.count()


class FollowSerializer(serializers.ModelSerializer):
    """关注序列化器"""
    follower_name = serializers.CharField(source='follower.user_name', read_only=True)
    following_name = serializers.CharField(source='following.user_name', read_only=True)
    follow_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = Follow
        fields = ['follow_id', 'follower', 'follower_name', 'following', 'following_name', 'follow_time']
        read_only_fields = ['follow_id', 'follow_time']


class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器"""
    log_user_type_display = serializers.CharField(source='get_log_user_type_display', read_only=True)
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = LoginLog
        fields = ['log_id', 'log_user', 'log_user_name', 'log_user_type', 'log_user_type_display', 'log_time']
        read_only_fields = ['log_id', 'log_time']

