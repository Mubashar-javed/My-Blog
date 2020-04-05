from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishManager(models.Manager):

    def get_queryset(self):
        queryset = super(PublishManager, self).get_queryset().filter(
            status='published')

        return queryset


class DraftManager(models.Manager):

    def get_queryset(self):
        queryset = super(DraftManager, self).get_queryset().filter(
            status='draft')

        return queryset


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique_for_date='publish', max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishManager()
    draft = DraftManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug,
                                                 ])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50, help_text='Your name here.')
    email = models.EmailField(blank=True, null=True,
                              help_text="Enter your Email Here!")
    body = models.TextField(help_text='Your comment here')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"comment by '{self.name}' on '{self.post}'"
