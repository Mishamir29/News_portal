import django_filters
from django import forms
from .models import Post

class PostsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название'
    )
    author__user__username = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора'
    )
    created_at = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата (позже чем)',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = []