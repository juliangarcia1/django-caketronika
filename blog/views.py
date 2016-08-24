#!/usr/bin/python
# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import (HttpResponseNotFound,
                         HttpResponse,
                         HttpResponseRedirect,
                         Http404,JsonResponse
                         )
# from haystack.query import SearchQuerySet
from django.db.models import Q
from django.shortcuts import render, get_object_or_404


from .forms import (LoginForm, UserRegistrationForm, PostForm,
                    CommentForm, SearchForm)
from .models import Post, Author, Category, VisitCounter


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def remove_tags(body):
    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(body)
    for tag in ['img','code']:
        for match in soup.findAll('code'):
            match.replaceWith('')
    return soup.text


def count_visitors(view_name):
    try:
        visits = VisitCounter.objects.get(view_name=view_name)
    except:
        visits = VisitCounter.objects.create(view_name=view_name, num_visits= 0)
    visits.num_visits += 1
    visits.save()

    return visits.num_visits


def home_view(request):
    posts = Post.objects.all().order_by('-created_at')

    post_previews={}
    for post in posts:
        post_previews.update({post.pk: remove_tags(post.body)})

    category_txt = ""

    num_visits = count_visitors('home_view')

    imgs_by_id = get_image_for_posts(posts)
    user_ip = get_client_ip(request)
    return render(request, 'blog/home.html', {'posts': posts,
                                         'post_previews': post_previews,
                                         'imgs_by_id':imgs_by_id,
                                         'num_visits':num_visits,
                                         'user_ip':user_ip,
                                         'category_txt':category_txt
                                         }
                  )


def get_first_image(html_str):
    import re
    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(html_str)
    img = soup.findAll('img')
    if img:
        return str(img[0]['src'])
    return ''


def get_image_for_posts(posts):
    imgs_by_id = {}
    for post in posts:
        body = post.body
        category = Category.objects.get(id=post.category_id)
        post_image = get_first_image((body))
        if post_image == '':
            category_image = category.image
            imgs_by_id.update({post.id: u'/media/'+category_image.name})
        else:
            imgs_by_id.update({post.id: post_image})
    return imgs_by_id


def article_list(request, category_pk=None, subcategory_pk=None):
    category_txt =""
    if category_pk is not None and subcategory_pk is not None:
        posts = Post.objects.filter(Q(category_id = category_pk) & Q(subcategory_id= subcategory_pk)).order_by('-created_at')
        if posts:
            category_txt = posts[0].category
    elif category_pk is not None:
        posts = Post.objects.filter(category_id = category_pk).order_by('-created_at')
        if posts:
            category_txt = posts[0].category
    else:
        posts = Post.objects.all().order_by('-created_at')
        category_txt = ""

    imgs_by_id = get_image_for_posts(posts)

    return render(request, 'blog/articulos.html',
                  {'posts':posts,
                   'imgs_by_id':imgs_by_id,
                   'category_txt':category_txt })

def ajax_send_comments(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.filter(active=True)
    import json

    return JsonResponse(json.dumps(comments))


def detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, 'Comentario enviado correctamente')
                HttpResponseRedirect( post.get_absolute_url() )
            else:
                messages.error(request, 'Necesitas estar registrarte para comentar')
                HttpResponseRedirect( post.get_absolute_url() )
    else:
        comment_form = CommentForm()
    return render(request,'blog/articulo_detalle.html',
                        {'post': post,
                         'comments':comments,
                         'comment_form':comment_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Logeado exitosamente')
                else:
                    return HttpResponse('Cuenta no habilitada')
            else:
                return HttpResponse('Login no valido')
    else:
        form = LoginForm()
    return render(request,'blog/login.html', {'form':form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html',
                          {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html',
                  {'user_form': user_form})


@login_required
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            if not hasattr(post, 'author'):
                author = Author.objects.create(
                    name = request.user.first_name,
                    last_name = request.user.last_name,
                    email = request.user.email
                )
                author.save()
                post.author = author
            else:
                post.author = request.user
            post.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Post created!')
            return HttpResponseRedirect(post.get_absolute_url())
    return render(request, 'blog/post_form.html',
                  {'form':form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post,pk=pk)

    form = PostForm(instance=post)
    category_txt = post.category

    if request.method == 'POST':
        form = PostForm(instance=post, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Updated {}'.format(form.cleaned_data['title']))
            return HttpResponseRedirect(post.get_absolute_url())
    return render(request, 'blog/edit_post.html',
                            {'form':form,
                             'post':post,
                             'category_txt':category_txt})


@login_required
def list_user_posts(request):
    posts = Post.objects.filter(author=request.user)
    imgs_by_id = get_image_for_posts(posts)
    category_txt = ""
    return render(request, 'blog/list_user_posts.html',
                  {'posts':posts,
                   'imgs_by_id':imgs_by_id,
                   'category_txt':category_txt})

