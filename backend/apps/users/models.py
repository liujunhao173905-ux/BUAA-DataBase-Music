"""
用户数据模型
基于系统设计报告中的用户表设计（表1）
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """用户管理器"""
    
    def create_user(self, user_name, password=None, **extra_fields):
        """创建普通用户"""
        if not user_name:
            raise ValueError('用户名是必填项')
        
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_name, password=None, **extra_fields):
        """创建超级管理员"""
        extra_fields.setdefault('user_type', 2)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(user_name, password, **extra_fields)


class User(AbstractBaseUser):
    """
    用户表（表1）
    用户类型：0-普通用户，1-歌手，2-管理员
    """
    USER_TYPES = (
        (0, '普通用户'),
        (1, '歌手'),
        (2, '管理员'),
    )
    
    user_id = models.AutoField(primary_key=True, verbose_name='用户ID')
    user_name = models.CharField(max_length=64, unique=True, verbose_name='用户名')
    user_mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    user_avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    user_createtime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    user_type = models.IntegerField(choices=USER_TYPES, default=0, verbose_name='用户类型')
    
    # Django认证系统必需字段
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_staff = models.BooleanField(default=False, verbose_name='是否员工')
    is_superuser = models.BooleanField(default=False, verbose_name='是否超级管理员')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='注册时间')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['user_name']),
            models.Index(fields=['user_type']),
        ]
    
    @property
    def id(self):
        """兼容需要使用 id 字段的库（如 SimpleJWT）"""
        return self.user_id
    
    def has_perm(self, perm, obj=None):
        """检查用户权限"""
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        """检查用户是否有访问应用的权限"""
        return self.is_superuser
    
    @property
    def is_normal_user(self):
        """是否为普通用户"""
        return self.user_type == 0
    
    @property
    def is_singer(self):
        """是否为歌手"""
        return self.user_type == 1
    
    @property
    def is_admin(self):
        """是否为管理员"""
        return self.user_type == 2


class Follow(models.Model):
    """
    用户关注表（表8）
    记录用户之间的关注关系
    """
    follow_id = models.AutoField(primary_key=True, verbose_name='关注ID')
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following_set',
        verbose_name='关注者',
        db_column='follower_id'
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='followers_set',
        verbose_name='被关注者',
        db_column='followed_id'
    )
    follow_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')
    
    class Meta:
        db_table = 'follows'
        verbose_name = '关注关系'
        verbose_name_plural = '关注关系'
        unique_together = ('follower', 'following')  # 防止重复关注
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]
    
    def __str__(self):
        return f'{self.follower.user_name} 关注 {self.following.user_name}'


class LoginLog(models.Model):
    """
    用户登录日志表（表9）
    记录用户每次登录的时间、用户类型等信息
    """
    log_id = models.AutoField(primary_key=True, verbose_name='日志ID')
    log_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_logs',
        verbose_name='用户',
        db_column='log_user_id'
    )
    log_user_name = models.CharField(max_length=64, verbose_name='用户名')
    log_user_type = models.IntegerField(choices=User.USER_TYPES, verbose_name='用户类型')
    log_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    
    class Meta:
        db_table = 'login_logs'
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        ordering = ['-log_time']
        indexes = [
            models.Index(fields=['log_user']),
            models.Index(fields=['log_time']),
        ]
    
    def __str__(self):
        return f'{self.log_user_name} 于 {self.log_time} 登录'

