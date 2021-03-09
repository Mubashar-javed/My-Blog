from django.contrib import admin
from .models import Post, Comment
from django.urls import reverse
from django.utils.html import format_html


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'slug', 'publish')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body', 'author')
    prepopulated_fields = {'slug': ('title',)}

    ordering = ('publish', 'status')
    date_hierarchy = 'publish'
    raw_id_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'created')
    list_filter = ('name', 'email', 'post', 'created')
    search_fields = ('name', 'email', 'post', 'body')
    ordering = ('created', 'active', 'email')
