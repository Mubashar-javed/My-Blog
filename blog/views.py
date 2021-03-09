from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import connections
from django.db.models import Q
from django.http import request
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post


def post_list(request, tag_slug=None):
    """ This will List all the Post in our
    **Template:**

    :template:`blog/post/list.html`
    """
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug, )
        object_list = object_list.filter(tags_in=[tag])

    paginator = Paginator(object_list, 3)  # this will show 3 post/page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {
        'page': page,
        'posts': posts,
        'tag': tag
    })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )

    # list of active comment for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    comment_form = CommentForm()
    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, 'blog/post/detail.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            if connections['default'].vendor == 'sqlite':
                # very basics search functionality
                results = Post.published.filter(
                    Q(title__icontains=query) | Q(body__icontains=query)
                )
            if connections['default'].vendor == 'postgresql':
                # builtin search method of postgresSql
                search_vector = SearchVector('title', 'body')
                search_query = SearchQuery(query)
                results = Post.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query)
                ).filter(search=search_query).order_by('-rank')
    ctx = {
        'form': form,
        'query': query,
        'results': results
    }
    return render(request, 'blog/post/search.html', context=ctx)
