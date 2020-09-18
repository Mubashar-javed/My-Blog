from django.contrib import admin
from .models import Post, Comment
from django.urls import reverse
from django.utils.html import format_html


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
    # skipping for now
    # readonly_fields = ('show_url',)

    # def show_url(self, instance):
    #     url = reverse('blog:post_detail', args=[instance.publish.year,
    #                                             instance.publish.month,
    #                                             instance.publish.day,
    #                                             instance.slug,
    #                                             ])
    #     response = format_html("""<a href="{0}">{0}</a> """, url)
    #     return response

    # show_url.short_description = "Blog Url here"
    # show_url.allow_tags = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'created')
    list_filter = ('name', 'email', 'post', 'created')
    search_fields = ('name', 'email', 'post', 'body')
    ordering = ('created', 'active', 'email')
