# Generated by Django 3.2.7 on 2021-12-14 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='カテゴリー')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=200, verbose_name='タイトル')),
                ('video', models.FileField(upload_to='video/%y')),
                ('thumb', models.FileField(blank=True, upload_to='thumb/%')),
                ('content', models.TextField(verbose_name='内容')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='video.category', verbose_name='カテゴリー')),
            ],
        ),
    ]
