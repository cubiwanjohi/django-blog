from django.contrib import admin
from django.db.models import Count
from .models import Category, Tag, Post, Comment


# ──────────────────────────────
# CATEGORY
# ──────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug', 'post_count')
    search_fields       = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            post_count=Count('posts')
        )

    @admin.display(description='Posts', ordering='post_count')
    def post_count(self, obj):
        return obj.post_count


# ──────────────────────────────
# TAG
# ──────────────────────────────
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug', 'post_count')
    search_fields       = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            post_count=Count('posts')
        )

    @admin.display(description='Posts', ordering='post_count')
    def post_count(self, obj):
        return obj.post_count


# ──────────────────────────────
# COMMENT (inline inside Post)
# ──────────────────────────────
class CommentInline(admin.TabularInline):
    model           = Comment
    extra           = 0
    fields          = ('author', 'guest_name', 'body', 'is_approved', 'created_at')
    readonly_fields = ('created_at',)


# ──────────────────────────────
# POST
# ──────────────────────────────
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display           = ('title', 'author', 'category', 'status', 'publish_date', 'views_count', 'allow_comments')
    list_filter            = ('status', 'category', 'tags', 'publish_date')
    search_fields          = ('title', 'body', 'meta_description')
    prepopulated_fields    = {'slug': ('title',)}
    date_hierarchy         = 'publish_date'
    ordering               = ('-publish_date',)
    readonly_fields        = ('views_count', 'created_at', 'updated_at')
    list_per_page          = 25
    show_full_result_count = False  # Avoids expensive COUNT(*) on large tables
    list_select_related    = ('author', 'category')  # Prevents N+1 on list page

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'body', 'excerpt', 'featured_image')
        }),
        ('Organisation', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Publication', {
            'fields': ('status', 'publish_date', 'allow_comments')
        }),
        ('SEO Metadata', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description')
        }),
        ('Stats', {
            'classes': ('collapse',),
            'fields': ('views_count', 'created_at', 'updated_at')
        }),
    )

    inlines = [CommentInline]
    actions = ['make_published', 'make_draft', 'make_archived']

    @admin.action(description='Mark selected posts as Published')
    def make_published(self, request, queryset):
        queryset.update(status=Post.Status.PUBLISHED)

    @admin.action(description='Mark selected posts as Draft')
    def make_draft(self, request, queryset):
        queryset.update(status=Post.Status.DRAFT)

    @admin.action(description='Mark selected posts as Archived')
    def make_archived(self, request, queryset):
        queryset.update(status=Post.Status.ARCHIVED)


# ──────────────────────────────
# COMMENT (standalone page)
# ──────────────────────────────
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display        = ('short_body', 'post', 'author_name', 'is_approved', 'created_at')
    list_filter         = ('is_approved', 'created_at')
    search_fields       = ('body', 'guest_name', 'guest_email')
    readonly_fields     = ('created_at',)
    list_select_related = ('post', 'author')  # Prevents N+1 on list page
    list_per_page       = 25
    actions             = ['approve_comments', 'reject_comments']

    @admin.display(description='Comment')
    def short_body(self, obj):
        return obj.body[:60] + '...' if len(obj.body) > 60 else obj.body

    @admin.display(description='Author')
    def author_name(self, obj):
        return obj.author.username if obj.author else f"{obj.guest_name} (guest)"

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Reject selected comments')
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)