from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    """Custom manager to return only published posts."""
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,   # If the user is deleted, delete all their posts
        related_name='blog_posts',
    )
    body = models.TextField()

    # Timestamps
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    objects = models.Manager() # Default manager
    published = PublishedManager() # Custom manager

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title