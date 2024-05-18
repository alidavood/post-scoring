from django.contrib import admin

from seedwork.admin import BaseAdmin
from .models import *


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('id', 'title',)
    ordering = ('-create_time',)


@admin.register(UserPostScore)
class UserPostScoreAdmin(BaseAdmin):
    list_display = ('id', 'post', 'user', 'score',)
    ordering = ('-create_time',)
    raw_id_fields = ('post', 'user',)


@admin.register(UserPostScoreHistory)
class UserPostScoreHistoryAdmin(BaseAdmin):
    list_display = ('id', 'user_post_score', 'score',)
    ordering = ('-create_time',)
    raw_id_fields = ('user_post_score',)
