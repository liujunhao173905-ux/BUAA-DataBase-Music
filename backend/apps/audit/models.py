"""
审核数据模型
基于系统设计报告中的审核日志表设计（表10-12）
"""
from django.db import models
from django.conf import settings


class CheckSongLog(models.Model):
    """
    歌曲审核日志表（表11）
    记录歌曲的审核历史，包含审核提交时的数据快照
    """
    CHECK_STATUS = (
        (0, '待审核'),
        (1, '审核通过'),
        (2, '审核拒绝'),
    )
    
    check_id = models.AutoField(primary_key=True, verbose_name='审核ID')
    check_song = models.ForeignKey(
        'music.Song',
        on_delete=models.CASCADE,
        related_name='check_logs',
        verbose_name='歌曲',
        db_column='check_song_id'
    )
    # 审核时的数据快照（历史记录）
    check_song_name = models.CharField(max_length=128, verbose_name='歌曲名称')
    check_song_cover = models.CharField(max_length=255, blank=True, null=True, verbose_name='歌曲封面路径')
    check_song_file = models.CharField(max_length=255, verbose_name='歌曲文件路径')
    check_song_duration = models.IntegerField(default=0, verbose_name='歌曲时长')
    check_song_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='歌曲价格')
    check_submit_time = models.DateTimeField(auto_now_add=True, verbose_name='审核提交时间')
    check_modify_time = models.DateTimeField(auto_now=True, verbose_name='审核修改时间')
    check_status = models.IntegerField(choices=CHECK_STATUS, default=0, verbose_name='审核状态')
    check_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checked_songs',
        verbose_name='审核管理员',
        limit_choices_to={'user_type': 2}  # 只允许管理员
    )
    check_comment = models.TextField(blank=True, null=True, verbose_name='审核意见')
    
    class Meta:
        db_table = 'check_song_logs'
        verbose_name = '歌曲审核日志'
        verbose_name_plural = '歌曲审核日志'
        ordering = ['-check_submit_time']
        indexes = [
            models.Index(fields=['check_song']),
            models.Index(fields=['check_status']),
            models.Index(fields=['check_submit_time']),
        ]
    
    def __str__(self):
        return f'{self.check_song_name} - {self.get_check_status_display()}'


class CheckPlaylistLog(models.Model):
    """
    歌单审核日志表（表10）
    记录歌单的审核历史，包含审核提交时的数据快照
    """
    CHECK_STATUS = (
        (0, '待审核'),
        (1, '审核通过'),
        (2, '审核拒绝'),
    )
    
    check_id = models.AutoField(primary_key=True, verbose_name='审核ID')
    check_playlist = models.ForeignKey(
        'playlists.Playlist',
        on_delete=models.CASCADE,
        related_name='check_logs',
        verbose_name='歌单',
        db_column='check_playlist_id'
    )
    # 审核时的数据快照（历史记录）
    check_playlist_name = models.CharField(max_length=128, verbose_name='歌单名称')
    check_playlist_cover = models.CharField(max_length=255, blank=True, null=True, verbose_name='歌单封面路径')
    check_playlist_intro = models.TextField(blank=True, null=True, verbose_name='歌单介绍')
    check_submit_time = models.DateTimeField(auto_now_add=True, verbose_name='审核提交时间')
    check_modify_time = models.DateTimeField(auto_now=True, verbose_name='审核修改时间')
    check_status = models.IntegerField(choices=CHECK_STATUS, default=0, verbose_name='审核状态')
    check_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checked_playlists',
        verbose_name='审核管理员',
        limit_choices_to={'user_type': 2}  # 只允许管理员
    )
    check_comment = models.TextField(blank=True, null=True, verbose_name='审核意见')
    
    class Meta:
        db_table = 'check_playlist_logs'
        verbose_name = '歌单审核日志'
        verbose_name_plural = '歌单审核日志'
        ordering = ['-check_submit_time']
        indexes = [
            models.Index(fields=['check_playlist']),
            models.Index(fields=['check_status']),
            models.Index(fields=['check_submit_time']),
        ]
    
    def __str__(self):
        return f'{self.check_playlist_name} - {self.get_check_status_display()}'


class CheckUserLog(models.Model):
    """
    用户审核日志表（表12）
    记录用户（特别是歌手）注册申请的审核历史
    """
    CHECK_STATUS = (
        (0, '待审核'),
        (1, '审核通过'),
        (2, '审核拒绝'),
    )
    
    check_id = models.AutoField(primary_key=True, verbose_name='审核ID')
    check_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='check_logs',
        verbose_name='用户',
        db_column='check_user_id'
    )
    # 审核时的数据快照（历史记录）
    check_user_name = models.CharField(max_length=64, verbose_name='用户名')
    check_user_mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    check_user_avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name='头像路径')
    check_user_type = models.IntegerField(verbose_name='用户类型')
    check_submit_time = models.DateTimeField(auto_now_add=True, verbose_name='审核提交时间')
    check_modify_time = models.DateTimeField(auto_now=True, verbose_name='审核修改时间')
    check_status = models.IntegerField(choices=CHECK_STATUS, default=0, verbose_name='审核状态')
    check_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checked_users',
        verbose_name='审核管理员',
        limit_choices_to={'user_type': 2}  # 只允许管理员
    )
    check_comment = models.TextField(blank=True, null=True, verbose_name='审核意见')
    
    class Meta:
        db_table = 'check_user_logs'
        verbose_name = '用户审核日志'
        verbose_name_plural = '用户审核日志'
        ordering = ['-check_submit_time']
        indexes = [
            models.Index(fields=['check_user']),
            models.Index(fields=['check_status']),
            models.Index(fields=['check_submit_time']),
        ]
    
    def __str__(self):
        return f'{self.check_user_name} - {self.get_check_status_display()}'

