from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm

class PostListView(ListView):
    """Alternative post list view using class-based views."""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request):
    """List all published posts."""
    posts = Post.published.all()

    # Pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If the requested page is out of range, return the last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If the requested page is not an integer, return the first page of results
        posts = paginator.page(1)

    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    """Display a single post."""
    post = get_object_or_404(
        Post, 
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post, 
        status=Post.Status.PUBLISHED,
    )
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    """Share a post via email."""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # TODO: Send email
        
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})
