from datetime import datetime

from django.core.exceptions import PermissionDenied

from .filters import PostsFilter
from .forms import PostForm
from .models import Post

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, DeleteView, CreateView, UpdateView
)
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def protected_view(request):
    return render(request, "protected.html")


@login_required
def upgrade_me(request):
    user = request.user
    if request.method == 'POST':
        try:
            # Получаем группу authors
            authors_group = Group.objects.get(name='authors')
            # Добавляем пользователя в эту группу
            user.groups.add(authors_group)
            # Правильно используем messages
            messages.success(request, "Поздравляем! Вы теперь автор.")
        except Group.DoesNotExist:
             messages.error(request, "Ошибка: группа авторов не найдена.")
        return redirect('/')

    # Проверим, не является ли пользователь уже автором
    is_author = user.groups.filter(name='authors').exists()
    return render(request, 'upgrade_me.html', {'is_author': is_author})


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    permission_required = 'news.add_post'
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


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    fields = ['title', 'content']
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.change_post'

    def get_queryset(self, queryset= None):
        obj = super().get_object(queryset)
        # Проверяем, является ли текущий пользователь автором объекта
        if not obj.author.user == self.request.user:
            raise PermissionDenied
        return obj


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

def news_search(request):
    queryset = Post.objects.all()
    filterset= PostsFilter(request.GET, queryset=queryset)
    return render(request, 'news_search.html', {'filterset': filterset,})


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


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'

    def get_queryset(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверяем, является ли текущий пользователь автором объекта
        if not obj.author.user == self.request.user:
            raise PermissionDenied
        return obj


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protected.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name = 'author').exists()
        return context
# Create your views here.