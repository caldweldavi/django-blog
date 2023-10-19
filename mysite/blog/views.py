from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm

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
    """Display a single post and its comments."""
    post = get_object_or_404(
        Post, 
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post, 
        status=Post.Status.PUBLISHED,
    )

    # Comments
    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})


def post_share(request, post_id):
    """Share a post via email."""

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Need to use build_absolute_url to include things like HTTP schema and hostname
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f'{cd['name']} reccomends that you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}'
            send_mail(subject, message, 'nonverbalgorilla@gmail.com', [cd['to']])
            sent = True
        
    else:
        # GET form
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    """Add a comment to a post, this requires a POST request."""

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    # Form was submitted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create comment object but don't save to database yet
        comment = form.save(commit=False)
        # Assign the current post to the comment
        comment.post = post
        comment.save()

    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})
