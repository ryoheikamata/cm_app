from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('カテゴリー', max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('add_category', kwargs={'pk': self.pk})


class Video(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    caption = models.CharField('タイトル', max_length=200)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    video = models.FileField(upload_to='video/%y')
    thumb = models.FileField(upload_to='thumb/%', blank=True)
    content = models.TextField('内容')
    created = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.caption
