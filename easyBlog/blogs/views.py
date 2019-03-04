from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Blog, BlogComment, Profile, ReplyComment
from .forms import BlogForm
import re

# Create your views here.
BLOG_PER_PAGE = 6
simple_query = None


def make_pagination(request, blogs):
    page = request.GET.get('page', 1)
    pagination = Paginator(blogs, BLOG_PER_PAGE)
    try:
        blogs = pagination.page(page)
    except PageNotAnInteger:
        blogs = pagination.page(1)
    except EmptyPage:
        blogs = pagination.page(pagination.num_pages)

    return blogs


def index(request, blogs=None):
    if blogs is None:
        blogs = Blog.objects.all()

    context = {
        'blogs': make_pagination(request, blogs)
    }

    return render(request, 'blogs/index.html', context)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        data = {
            'blog': blog,
            'author': request.user,
            'text': request.POST['comment']
        }
        BlogComment.objects.create(**data)

    blog_comments = BlogComment.objects.filter(blog=blog)
    sum_comments = blog_comments.all().count()
    context = {
        'blog': blog,
        'blog_comments': make_pagination(request, blog_comments),
        'blog_comments_sum': sum_comments
    }

    return render(request, 'blogs/blog_detail.html', context)


@login_required
def reply_comment(request, blog_comment_id):
    blog_comment = BlogComment.objects.get(pk=blog_comment_id)
    blog = blog_comment.blog

    data = {
        'comment': blog_comment,
        'author': request.user,
        'text': request.POST['reply_comment']
    }

    r = ReplyComment.objects.create(**data)
    blog_comment.reply_comments.add(r)
    blog_comments = BlogComment.objects.filter(blog=blog)
    sum_comments = blog_comments.all().count()

    context = {
        'blog': blog,
        'blog_comments': make_pagination(request, blog_comments),
        'blog_comments_sum': sum_comments
    }

    return render(request, 'blogs/blog_detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.author = request.user
            stock.save()
            messages.success(request, f'创建博客成功!')
            return redirect('blogs:index')
    else:
        form = BlogForm()
    return render(request, 'blogs/create.html', {'form': form})


def search(request):
    global simple_query
    tmp = request.GET.get('easy_search')
    if tmp is not None:
        simple_query = tmp
    words = re.split(r'\s+', simple_query.strip())
    if len(words) == 0 or (len(words) == 1 and words[0] == ''):
        return redirect('blogs:index')
    blogs = Blog.objects.all()
    for word in words:
        blogs = blogs.filter(
            Q(title__icontains=word) |
            Q(subtitle__icontains=word) |
            Q(label__icontains=word) |
            Q(text__icontains=word) |
            Q(author__username__icontains=word) |
            Q(blog_like_users__username__icontains=word)
        ).distinct()

    blogs = blogs.order_by('-blog_like_users')

    context = {
        'blogs': make_pagination(request, blogs)
    }

    return render(request, 'blogs/index.html', context)


@login_required
def view_profile(request):
    user = request.user
    blogs = Blog.objects.filter(author=user)
    sum_like_num = 0
    for blog in blogs:
        sum_like_num += blog.blog_like_users.all().count()
    context = {
        'user': user,
        'blogs': make_pagination(request, blogs),
        'sum_like_num': sum_like_num
    }
    return render(request, 'blogs/view_profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        user.profile.label = request.POST['label']
        user.profile.introduction = request.POST['introduction']
        user.profile.header = request.FILES.get('header')
        user.profile.save()
        return redirect('blogs:view_profile')
    return render(request, 'blogs/edit_profile.html')


@login_required
def profile_like_blogs(request):
    user = request.user
    like_blogs = user.profile.user_like_blogs.all()

    context = {
        'blogs': make_pagination(request, like_blogs)
    }

    return render(request, 'blogs/like_blogs.html', context)


@login_required
def profile_follow_users(request):
    user = request.user
    follow_users = user.profile.follow_users.all()

    context = {
        'follow_users': make_pagination(request, follow_users)
    }

    return render(request, 'blogs/follow_users.html', context)


@login_required
def profile_fan_users(request):
    user = request.user
    fan_users = user.profile.fan_users.all()

    context = {
        'fan_users': make_pagination(request, fan_users)
    }

    return render(request, 'blogs/fan_users.html', context)


@login_required
def view_other_profile(request, user_id):
    other_user = User.objects.get(pk=user_id)
    blogs = Blog.objects.filter(author=other_user)
    sum_like_num = 0
    for blog in blogs:
        sum_like_num += blog.blog_like_users.all().count()

    context = {
        'user': other_user,
        'blogs': make_pagination(request, blogs),
        'sum_like_num': sum_like_num
    }
    return render(request, 'blogs/view_other_profile.html', context)


@login_required
def add_like_blog(request):
    blog = Blog.objects.get(pk=request.POST.get('blog_id'))
    user = request.user
    if user not in blog.blog_like_users.all():
        data = 'add'
        blog.blog_like_users.add(user)
        blog.save()
        user.profile.user_like_blogs.add(blog)
        user.save()
    else:
        data = 'remove'
        blog.blog_like_users.remove(user)
        blog.save()
        user.profile.user_like_blogs.remove(blog)
        user.save()
    return HttpResponse(data)


@login_required
def add_fan_and_follow_users(request):
    user = request.user
    blog = Blog.objects.get(pk=request.POST.get('blog_id'))
    if user != blog.author:
        if user not in blog.author.profile.fan_users.all():
            data = 'add'
            blog.author.profile.fan_users.add(user)
            blog.save()
            user.profile.follow_users.add(blog.author)
            user.save()
        else:
            data = 'remove'
            blog.author.profile.fan_users.remove(user)
            blog.save()
            user.profile.follow_users.remove(blog.author)
            user.save()
    else:
        data = 'self'
    return HttpResponse(data)


@login_required
def vote_blog_comment(request):
    user = request.user
    blog_comment = BlogComment.objects.get(pk=request.POST.get('blog_comment_id'))
    if user not in blog_comment.comment_like_users.all():
        data = 'up'
        blog_comment.comment_like_users.add(user)
        blog_comment.save()
    else:
        data = 'down'
        blog_comment.comment_like_users.remove(user)
        blog_comment.save()
    return HttpResponse(data)


@login_required
def vote_reply_comment(request):
    user = request.user
    reply_new_comment = ReplyComment.objects.get(pk=request.POST.get('reply_comment_id'))
    if user not in reply_new_comment.reply_comment_like_users.all():
        data = 'up'
        reply_new_comment.reply_comment_like_users.add(user)
        reply_new_comment.save()
    else:
        data = 'down'
        reply_new_comment.reply_comment_like_users.remove(user)
        reply_new_comment.save()
    return HttpResponse(data)


@login_required
def delete_blog(request, blog_id):
    Blog.objects.get(pk=blog_id).delete()
    return redirect('../../blog/view_profile')


# def delete_users(request):
#     User.objects.get(username='macbook').delete()
#     return HttpResponse('OK')