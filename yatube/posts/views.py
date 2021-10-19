from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Group
from .forms import PostForm
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    template = 'posts/index.html'
    posts_all = Post.objects.all()

    paginator = Paginator(posts_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts_all = group.posts.all()

    paginator = Paginator(posts_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts_all = author.posts.all()
    posts_count = author.posts.count()

    paginator = Paginator(posts_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'posts_count': posts_count,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    post_slice = post.text[0:30]
    posts_count = post.author.posts.count()

    context = {
        'post': post,
        'post_slice': post_slice,
        'posts_count': posts_count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    if request.method == 'POST':
        post_temp = Post(author=request.user)
        form = PostForm(request.POST, instance=post_temp)

        if form.is_valid():
            form.save()
            return redirect('posts:profile', username=request.user.username)

        return render(request, 'posts/create_post.html', {'form': form})
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('/posts/' + str(post_id))

        return render(request, 'posts/create_post.html', {
            'form': form,
            'is_edit': is_edit,
            'post_id': post_id,
        })

    form = PostForm(instance=post)

    return render(request, 'posts/create_post.html', {
        'form': form,
        'is_edit': is_edit,
        'post_id': post_id,
    })
