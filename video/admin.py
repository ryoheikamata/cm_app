from django.contrib import admin
from .models import Video, Category

# admin.site.register(Video)
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'caption', 'category', 'video', 'created')
    list_display_links = ('caption',)
    ordering = ('created',)

# admin.site.register(Category)
@admin.register(Category)
class CtegoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
