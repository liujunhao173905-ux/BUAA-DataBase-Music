# songs/migrations/000X_convert_is_active_to_status.py
from django.db import migrations
from django.db import models

def bool_to_int(apps, schema_editor):
    Playlist = apps.get_model('playlists', 'Playlist')

    # 歌单同理
    for p in Playlist.objects.all():
        p.playlist_status = 1 if p.is_active else 0
    Playlist.objects.bulk_update(Playlist.objects.all(), ['playlist_status'])

class Migration(migrations.Migration):
    dependencies = [('playlists', '0001_initial')]
    operations = [
        migrations.AlterIndexTogether(
            name='playlist',
            index_together=set(),   # 如果还有联合索引一起清
        ),
        migrations.RemoveIndex(
            model_name='playlist',
            name='playlists_is_acti_8c1cb3_idx',  # 这是 Django 给 is_active 的默认索引名
        ),


        # 1. 新增整数字段（默认 0）
        migrations.AddField(
            model_name='playlist',
            name='playlist_status',
            field=models.IntegerField(choices=[(0, '审核中'), (1, '审核通过'), (2, '审核未通过'), (3, '已锁定')], default=0),
        ),

        # 2. 把旧 bool 值拷贝到新字段
        migrations.RunPython(bool_to_int, reverse_code=migrations.RunPython.noop),

        # 3. 删除旧字段
        migrations.RemoveField(model_name='playlist', name='is_active'),

        # 4. 给新字段加索引（可选）
        migrations.AddIndex(
            model_name='playlist',
            index=models.Index(fields=['playlist_status'], name='playlist_status_idx'),
        ),
    ]