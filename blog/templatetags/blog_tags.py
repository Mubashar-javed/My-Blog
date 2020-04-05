import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from blog.models import Post

"""the name of this file is important, we will use this module to load our custom tags................
 `simple_tag`:Process the data and return a string.
    `inclusion_tag:`  Process the data and return a rendered template
 """
register = template.Library()


@register.simple_tag
def total_posts():
    # our new template tag name is total_post (the name of our post.)
    return Post.published.count()


@register.inclusion_tag('blog\post\latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


# if we specify the name in decorator then it will be used in our templates
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
