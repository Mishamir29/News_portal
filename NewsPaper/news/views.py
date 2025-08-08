from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Author


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
# Create your views here.
