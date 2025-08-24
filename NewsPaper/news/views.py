from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, DeleteView, CreateView, UpdateView
)
from .filters import PostsFilter
from .forms import PostForm
from .models import Post
from django.shortcuts import render



class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        news_path = "/post/news/create/"
        if self.request.path == news_path:
            post.post_type = "NW"
        else:
            post.post_type = "AR"
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_type"] = 'новость' if self.request.path == "/post/news/create/" else 'статью'
        return context


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = None
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


def news_search(request):
    queryset = Post.objects.all()
    filterset= PostsFilter(request.GET, queryset=queryset)
    return render(request, 'news_search.html', {'filterset': filterset,})


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'post_confirm_delete.html'


    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author__user=self.request.user)


# Create your views here.
