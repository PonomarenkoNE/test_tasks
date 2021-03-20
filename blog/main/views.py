from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .form import UserForm, RegForm, CommentForm, PostForm
from .models import Post, Comment


@login_required(login_url='home')
def root(request):
    return redirect('blog')


def registration(request):
    is_exist = False
    fields_not_filled = False
    if request.method == 'POST':
        form = RegForm(request.POST)
        is_exist = True if (User.objects.filter(username=form.instance.username).exists()
                            or User.objects.filter(email=form.instance.email).exists()) else False
        if form.is_valid():
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'),
                                            request.POST.get('password'))
            login(request, user)
            return redirect(reverse('blog'))
        else:
            fields_not_filled = True
    form = RegForm()
    context = {
        'form': form,
        'fl1': is_exist,
        'fl2': fields_not_filled
    }
    return render(request, 'registration.html', context)


def home(request):
    uncorrect_user = False
    if request.method == 'POST':
        try:
            uncorrect_user = False
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect(reverse('blog'))
            else:
                uncorrect_user = True
        except Exception:
            return render(request, 'home.html', {'form': UserForm(), 'fl': uncorrect_user})
    form = UserForm()
    context = {
        'form': form,
        'fl': uncorrect_user
    }
    return render(request, 'login.html', context)


def loggout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='home')
def blog(request):
    posts = Post.objects.all()
    coms = Comment.objects.all()
    context = {
        'posts': posts,
        'request': request,
        'form': CommentForm(),
        'comments': coms,
    }
    return render(request, 'blog.html', context)


@login_required(login_url='home')
def profile(request):
    posts = Post.objects.filter(from_user=request.user)
    context = {
        'username': request.user.username,
        'posts': posts,
        'fl': True,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='home')
def addcomment(request, _id):
    if Post.objects.filter(id=_id).exists():
        obj = Post.objects.get(id=_id)
    else:
        return
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(text=form.cleaned_data['text'], from_user=request.user, to_post=obj)
            return redirect('blog')


@login_required(login_url='home')
def deletepost(request, _id):
    if Post.objects.filter(id=_id).exists():
        obj = Post.objects.get(id=_id)
    else:
        return
    if request.method == 'GET':
        if request.user == obj.from_user or request.user.is_superuser:
            Post.objects.get(id=_id).delete()
    return redirect('profile')


@login_required(login_url='home')
def add_post(request):
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(from_user=user, text=form.cleaned_data['text'], header=form.cleaned_data['header'],
                                picture=form.cleaned_data['picture'])
            return redirect(reverse('profile'))
    context = {
        'form': PostForm(),
    }
    return render(request, 'addpost.html', context)


@login_required(login_url='home')
def edit(request, _id):
    if Post.objects.filter(id=_id).exists():
        obj = Post.objects.get(id=_id)
    else:
        return
    form = PostForm()
    form.text = obj.text
    form.header = obj.header
    form.picture = obj.picture
    context = {'form': form, 'post': obj}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj.text = form.cleaned_data['text']
            if obj.picture is not None:
                obj.picture = form.cleaned_data['picture']
            obj.header = form.cleaned_data['header']
            obj.save()
            return redirect(reverse('profile'))
    return render(request, 'edit.html', context)

