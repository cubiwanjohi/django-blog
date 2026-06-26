from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag, Comment
from .forms import CommentForm, SearchForm


# ──────────────────────────────
# POST LIST
# ──────────────────────────────
def post_list(request):
    """Show all published posts with pagination."""
    posts = Post.published.all().select_related('author', 'category')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
    })


# ──────────────────────────────
# POST DETAIL
# ──────────────────────────────
def post_detail(request, year, month, day, slug):
    """Show a single post and its approved comments."""
    post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.Status.PUBLISHED,
        publish_date__year=year,
        publish_date__month=month,
        publish_date__day=day,
    )

    # Increment view count
    Post.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)

    # Only fetch top-level approved comments (replies handled in template)
    comments = post.comments.approved().filter(parent=None).select_related('author')

    # Pass a blank comment form to the template
    form = CommentForm(user=request.user)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


# ──────────────────────────────
# CATEGORY DETAIL
# ──────────────────────────────
def category_detail(request, slug):
    """Show all published posts in a category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category).select_related('author')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category_detail.html', {
        'category': category,
        'page_obj': page_obj,
    })


# ──────────────────────────────
# TAG DETAIL
# ──────────────────────────────
def tag_detail(request, slug):
    """Show all published posts with a given tag."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.published.filter(tags=tag).select_related('author', 'category')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/tag_detail.html', {
        'tag': tag,
        'page_obj': page_obj,
    })


# ──────────────────────────────
# SEARCH
# ──────────────────────────────
def search(request):
    """Search posts by title, body, or excerpt."""
    form = SearchForm(request.GET)
    posts = Post.objects.none()
    query = ''

    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        if query:
            posts = Post.published.filter(
                Q(title__icontains=query)   |
                Q(body__icontains=query)    |
                Q(excerpt__icontains=query)
            ).select_related('author', 'category').distinct()

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/search.html', {
        'form': form,
        'query': query,
        'page_obj': page_obj,
    })


# ──────────────────────────────
# ADD COMMENT
# ──────────────────────────────
def add_comment(request, year, month, day, slug):
    """Handle comment form submission. POST only."""
    post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.Status.PUBLISHED,
        publish_date__year=year,
        publish_date__month=month,
        publish_date__day=day,
    )

    if request.method != 'POST':
        return redirect('blog:post_detail', year=year, month=month, day=day, slug=slug)

    if not post.allow_comments:
        messages.error(request, 'Comments are disabled for this post.')
        return redirect('blog:post_detail', year=year, month=month, day=day, slug=slug)

    form = CommentForm(request.POST, user=request.user)

    if form.is_valid():
        comment = form.save(commit=False)  # don't save to DB yet
        comment.post = post                # attach the post
        if request.user.is_authenticated:
            comment.author = request.user  # attach logged-in user
        comment.save()
        messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
    else:
        messages.error(request, 'Please fix the errors in your comment.')

    return redirect('blog:post_detail', year=year, month=month, day=day, slug=slug)


# ──────────────────────────────
# AUTH IMPORTS
# ──────────────────────────────
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


# ──────────────────────────────
# REGISTER
# ──────────────────────────────
def register(request):
    """Register a new user account."""
    # Redirect already logged-in users away from register page
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in immediately after registering
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('blog:post_list')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


# ──────────────────────────────
# LOGIN
# ──────────────────────────────
def user_login(request):
    """Log in an existing user."""
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the page they were trying to visit, or post list
            next_url = request.GET.get('next', 'blog:post_list')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'blog/login.html')


# ──────────────────────────────
# LOGOUT
# ──────────────────────────────
@login_required
def user_logout(request):
    """Log out the current user. POST only for security."""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('blog:post_list')


# ──────────────────────────────
# PROFILE
# ──────────────────────────────
@login_required
def profile(request):
    """Show the logged-in user's posts and comments."""
    user_posts = Post.objects.filter(
        author=request.user
    ).order_by('-publish_date')

    user_comments = Comment.objects.filter(
        author=request.user
    ).order_by('-created_at')[:10]  # last 10 comments

    return render(request, 'blog/profile.html', {
        'user_posts': user_posts,
        'user_comments': user_comments,
    })