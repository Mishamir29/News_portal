from django.shortcuts import render
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView
)
from .filters import PostsFilter
from .forms import PostForm
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

NEWS = 'NW'
ARTICLE = 'AR'


@login_required
def post_create(request, post_type):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_type= post_type
            post.author = request.user
            post.save()
            return redirect('post_list')
        else:
            form = PostForm()
        return render(request, 'post_create.html', {
            'form': form,
            'post_type': 'новость' if post_type == NEWS else 'статью'
        })


@login_required
def post_edit(request, pk, post_type):
    post = get_object_or_404(Post,pk=pk)
    if post.post_type != post_type:
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, instance= post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {
        'form': form,
        'post': post
    })


@require_http_methods(["POST"])
@login_required
def post_delete(request, pk, post_type):
    post = get_object_or_404(Post, pk=pk)
    if post.post_type != post_type:
        return redirect('post_list')
    post.delete()
    return redirect('post_list')


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
    queryset = Post.objects.filter(post_type= 'news')
    filterset= PostsFilter(request.GET, queryset=queryset)
    return render(request, 'news_search.html', {'filterset': filterset,})


# Create your views here.
