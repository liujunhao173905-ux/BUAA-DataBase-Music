"""
歌单数据模型
基于系统设计报告中的歌单表设计（表2）
"""
from django.db import models
from django.conf import settings


class Playlist(models.Model):
    """
    歌单表（表2）
    存储歌单的基本信息
    """
    playlist_id = models.AutoField(primary_key=True, verbose_name='歌单ID')
    playlist_name = models.CharField(max_length=128, verbose_name='歌单名称')
    playlist_cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name='歌单封面')
    playlist_intro = models.TextField(blank=True, null=True, verbose_name='歌单介绍')
    playlist_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_playlists',
        verbose_name='创建者',
        db_column='user_id'
    )
    playlist_createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    playlist_updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    playlist_status = models.PositiveSmallIntegerField(
        choices=[(0, '审核中'), (1, '已上架'), (2, '未过审'), (3, '已锁定')],
        default=0,
        db_index=True,
        verbose_name='歌单状态'
    )
    
    class Meta:
        db_table = 'playlists'
        verbose_name = '歌单'
        verbose_name_plural = '歌单'
        ordering = ['-playlist_createtime']
        indexes = [
            models.Index(fields=['playlist_name']),
            models.Index(fields=['playlist_creator']),
            models.Index(fields=['playlist_status']),
        ]
    
    def __str__(self):
        return self.playlist_name


class PlaylistSong(models.Model):
    """
    歌单歌曲表（表4）
    记录歌单中包含的歌曲
    """
    playlist_songs_id = models.AutoField(primary_key=True, verbose_name='歌单歌曲项ID')
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='songs',
        verbose_name='歌单',
        db_column='playlist_id'
    )
    song = models.ForeignKey(
        'music.Song',
        on_delete=models.CASCADE,
        related_name='in_playlists',
        verbose_name='歌曲',
        db_column='song_id'
    )
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    order = models.IntegerField(default=0, verbose_name='排序顺序')
    
    class Meta:
        db_table = 'playlist_songs'
        verbose_name = '歌单歌曲'
        verbose_name_plural = '歌单歌曲'
        unique_together = ('playlist', 'song')  # 防止重复添加
        ordering = ['order', 'add_time']
        indexes = [
            models.Index(fields=['playlist']),
            models.Index(fields=['song']),
        ]
    
    def __str__(self):
        return f'{self.playlist.playlist_name} - {self.song.song_name}'


class StarPlaylist(models.Model):
    """
    用户收藏歌单表（表5）
    记录用户收藏的歌单
    """
    star_playlist_id = models.AutoField(primary_key=True, verbose_name='收藏歌单ID')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='starred_playlists',
        verbose_name='用户',
        db_column='user_id'
    )
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='starred_by',
        verbose_name='歌单',
        db_column='playlist_id'
    )
    star_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    
    class Meta:
        db_table = 'star_playlists'
        verbose_name = '收藏歌单'
        verbose_name_plural = '收藏歌单'
        unique_together = ('user', 'playlist')  # 防止重复收藏
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['playlist']),
        ]
    
    def __str__(self):
        return f'{self.user.user_name} 收藏 {self.playlist.playlist_name}'

