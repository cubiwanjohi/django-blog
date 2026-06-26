from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# ──────────────────────────────
# CATEGORY
# ──────────────────────────────
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug_candidate = base_slug
            counter = 1
            # Increment counter until a unique slug is found
            while Category.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ──────────────────────────────
# TAG
# ──────────────────────────────
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug_candidate = base_slug
            counter = 1
            # Same simple counter approach as Category — consistent and readable
            while Tag.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ──────────────────────────────
# POST MANAGERS
# ──────────────────────────────
class PublishedManager(models.Manager):
    """Returns only published posts. Usage: Post.published.all()"""
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# ──────────────────────────────
# POST
# ──────────────────────────────
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    # Core content
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    body = models.TextField()
    excerpt = models.TextField(blank=True)

    # Media
    featured_image = models.ImageField(
        upload_to='posts/%Y/%m/%d/', blank=True, null=True
    )

    # Relationships
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    # Publication state
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    publish_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO Metadata
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Engagement
    views_count = models.PositiveIntegerField(default=0)
    allow_comments = models.BooleanField(default=True)

    # Managers
    objects = models.Manager()       # All posts (default)
    published = PublishedManager()   # Published posts only

    class Meta:
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['-publish_date']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.excerpt:
            # Trim to 200 chars without cutting mid-word
            trimmed = self.body[:203]
            self.excerpt = trimmed[:trimmed.rfind(' ')] if ' ' in trimmed else trimmed[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ──────────────────────────────
# COMMENT MANAGERS
# ──────────────────────────────
class CommentManager(models.Manager):
    """Returns only approved comments. Usage: Comment.approved.all()"""
    def get_queryset(self):
        return super().get_queryset().filter(is_approved=True)


# ──────────────────────────────
# COMMENT
# ──────────────────────────────
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    # Logged-in user (null if guest)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    # Guest details (only filled if author is null)
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    # Self-referential FK for nested replies
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='replies'
    )

    # Managers
    objects = models.Manager()      # All comments (for admin/moderation)
    approved = CommentManager()     # Approved comments only (for public)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def clean(self):
        """Enforce: a comment must have either a logged-in author OR a guest name — not both, not neither."""
        if self.author and (self.guest_name or self.guest_email):
            raise ValidationError("Logged-in users should not provide guest details.")
        if not self.author and not self.guest_name:
            raise ValidationError("Guest comments must include a name.")

    def __str__(self):
        name = self.author.username if self.author else self.guest_name
        return f"Comment by {name} on '{self.post.title}'"