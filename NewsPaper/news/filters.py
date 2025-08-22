from django.forms import DateTimeField, DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import Post, Author


class PostsFilter(FilterSet):
    title = CharFilter(
        field_name= 'title',
        lookup_expr='icontains',
        label= 'Название содержит',
    )
    author = CharFilter(
        field_name= 'author__user__username',
        lookup_expr= 'icontains',
        label= 'Имя автора содержит'

    )
    created_after= DateTimeField(
        label= 'Дата от',
        widget= DateTimeInput(
            attrs={'type': 'datetime-local'}
        ),
    )


    class Meta:
        model = Post
        fields = []