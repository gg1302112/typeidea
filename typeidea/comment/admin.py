from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'create_time')
