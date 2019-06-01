from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.db.models.aggregates import Sum
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)
from embed_video.fields import EmbedVideoField

from wykop.accounts.models import User
from wykop.posts.forms import CommentForm
from wykop.posts.models import Comment

from .models import Post

# def hello_world(request):
#     print(request)
#     # return HttpResponse('<b>Hello world!</b>')
#     return render(request, 'posts/index.html')

# class HelloWorldView(View):
#     def get(self, request, *args, **kwargs):
#           return render(request, 'posts/index.html')

class HelloWorldView(TemplateView):
    template_name = 'base.html'
class Item(models.Model):
    video = EmbedVideoField()  # same like models.URLField()

class PostList(ListView):
    template_name = 'posts/list.html'
    # queryset = Post.objects.filter(published=True)
    model = Post
    paginate_by = 3
    ordering='-created'
    extra_context = {
        'title': 'Wpisy',
    }

class TopPostList(PostList):
    queryset = Post.objects.annotate(score=Sum('votes__value')).order_by('-score')
    ordering = ''

class PostDetail(DetailView):
    template_name = 'posts/detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = self.object.title
        data['comment_form'] = CommentForm()
        return data


class PostCreate(LoginRequiredMixin, CreateView):
    
    template_name = 'posts/create.html'
    model = Post
    fields = ['title', 'text', 'image','video']
    extra_context = {
        'title': 'Dodawanie wpisu',
    }
    def dispatch(self, request, *args, **kwargs):
        if request.user.banned:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'posts/update.html'
    model = Post
    fields = ['title', 'text', 'image']

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Edycja ' + self.object.title
        return data


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'posts/delete.html'
    model = Post
    success_url = reverse_lazy('posts:list')

    def test_func(self):
        obj = self.get_object()
        return (
            (self.request.user == obj.author) and
            (timezone.now() - obj.created < timedelta(0, 15*60))
        )

class CommentCreateView(LoginRequiredMixin,CreateView):
    model=Comment
    fields = ['text']
    def get_post(self):
        post_pk=self.kwargs.get('post_pk')
        return Post.objects.get(pk=post_pk)

    def form_valid(self, form):
        
        form.instance.user = self.request.user
        form.instance.post = self.get_post()
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.get_post().get_absolute_url()