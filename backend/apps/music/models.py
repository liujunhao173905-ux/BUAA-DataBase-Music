"""
音乐数据模型
基于系统设计报告中的歌曲表设计（表3）
"""
from django.db import models
from django.conf import settings


class Song(models.Model):
    """
    歌曲表（表3）
    存储歌曲的基本信息和文件路径
    """
    song_id = models.AutoField(primary_key=True, verbose_name='歌曲ID')
    song_name = models.CharField(max_length=128, verbose_name='歌曲名称')
    song_cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name='歌曲封面')
    song_file = models.FileField(upload_to='songs/', verbose_name='歌曲文件路径')
    song_duration = models.IntegerField(default=0, verbose_name='歌曲时长（秒）')
    song_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='歌曲价格')
    song_singer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='songs',
        verbose_name='歌手',
        limit_choices_to={'user_type': 1}  # 只允许歌手类型
    )
    song_createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    song_updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    song_status = models.PositiveSmallIntegerField(
        choices=[(0, '审核中'), (1, '已上架'), (2, '未过审'), (3, '已锁定')],
        default=0,
        db_index=True,
        verbose_name='歌曲状态'
    )
    
    class Meta:
        db_table = 'songs'
        verbose_name = '歌曲'
        verbose_name_plural = '歌曲'
        ordering = ['-song_createtime']
        indexes = [
            models.Index(fields=['song_name']),
            models.Index(fields=['song_singer']),
            models.Index(fields=['song_status']),
        ]
    
    def __str__(self):
        return self.song_name


class StarSong(models.Model):
    """
    用户收藏歌曲表（表6）
    记录用户收藏的歌曲
    """
    star_song_id = models.AutoField(primary_key=True, verbose_name='收藏歌曲ID')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='starred_songs',
        verbose_name='用户',
        db_column='user_id'
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='starred_by',
        verbose_name='歌曲',
        db_column='song_id'
    )
    star_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    
    class Meta:
        db_table = 'star_songs'
        verbose_name = '收藏歌曲'
        verbose_name_plural = '收藏歌曲'
        unique_together = ('user', 'song')  # 防止重复收藏
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['song']),
        ]
    
    def __str__(self):
        return f'{self.user.user_name} 收藏 {self.song.song_name}'


class BuySong(models.Model):
    """
    用户购买歌曲表（表7）
    记录用户购买的收费歌曲
    """
    buy_song_id = models.AutoField(primary_key=True, verbose_name='购买记录ID')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bought_songs',
        verbose_name='用户',
        db_column='user_id'
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='bought_by',
        verbose_name='歌曲',
        db_column='song_id'
    )
    buy_time = models.DateTimeField(auto_now_add=True, verbose_name='购买时间')
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='购买价格')
    
    class Meta:
        db_table = 'buy_songs'
        verbose_name = '购买歌曲'
        verbose_name_plural = '购买歌曲'
        unique_together = ('user', 'song')  # 防止重复购买
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['song']),
            models.Index(fields=['buy_time']),
        ]
    
    def __str__(self):
        return f'{self.user.user_name} 购买 {self.song.song_name}'


class PlayHistory(models.Model):
    """
    用户播放记录表
    记录用户的听歌历史，用于生成统计报告
    """
    history_id = models.AutoField(primary_key=True, verbose_name='播放记录ID')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='play_history',
        verbose_name='用户',
        db_column='user_id'
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='play_history',
        verbose_name='歌曲',
        db_column='song_id'
    )
    play_time = models.DateTimeField(auto_now_add=True, verbose_name='播放时间')
    play_duration = models.IntegerField(default=0, verbose_name='播放时长(秒)')
    
    class Meta:
        db_table = 'play_history'
        verbose_name = '播放记录'
        verbose_name_plural = '播放记录'
        ordering = ['-play_time']
        indexes = [
            models.Index(fields=['user', 'play_time']),
        ]
    
    def __str__(self):
        return f'{self.user.user_name} 播放 {self.song.song_name}'
