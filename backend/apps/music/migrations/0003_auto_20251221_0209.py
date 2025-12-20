# songs/migrations/000X_convert_is_active_to_status.py
from django.db import migrations
from django.db import models

def bool_to_int(apps, schema_editor):
    Song = apps.get_model('music', 'Song')
    # 歌曲：True→1，False→0
    for s in Song.objects.all():
        s.song_status = 1 if s.is_active else 0
    Song.objects.bulk_update(Song.objects.all(), ['song_status'])

class Migration(migrations.Migration):
    dependencies = [('music', '0002_playhistory')]
    operations = [
        migrations.AlterIndexTogether(
            name='song',
            index_together=set(),   # 如果还有联合索引一起清
        ),
        migrations.RemoveIndex(
            model_name='song',
            name='songs_is_acti_d12d51_idx',  # 这是 Django 给 is_active 的默认索引名
        ),


        # 1. 新增整数字段（默认 0）
        migrations.AddField(
            model_name='song',
            name='song_status',
            field=models.IntegerField(choices=[(0, '审核中'), (1, '已上架'), (2, '未过审'), (3, '已锁定')], default=0),
        ),

        # 2. 把旧 bool 值拷贝到新字段
        migrations.RunPython(bool_to_int, reverse_code=migrations.RunPython.noop),

        # 3. 删除旧字段
        migrations.RemoveField(model_name='song', name='is_active'),

        # 4. 给新字段加索引（可选）
        migrations.AddIndex(
            model_name='song',
            index=models.Index(fields=['song_status'], name='song_status_idx'),
        ),
    ]