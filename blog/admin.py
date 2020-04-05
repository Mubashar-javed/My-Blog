from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # this is our displaying format
    list_display = ('title', 'author', 'status', 'slug', 'publish')
    # this is just adding filter to the search filed
    list_filter = ('status', 'created', 'publish', 'author')
    # mean you can search item by title and body
    search_fields = ('title', 'body', 'author')
    # this will populate out slug field according to its title
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
