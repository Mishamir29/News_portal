from django.urls import path
from . import views
from .views import NewsList, NewsDetail

NEWS = 'NW'
ARTICLE = 'AR'


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>/',NewsDetail.as_view(), name= 'news_detail'),
    path('search/',views.news_search, name='news_search'),
    path('create/', lambda request: views.post_create(request, post_type=NEWS), name='news_create'),
    path('<int:pk>/edit/', lambda request, pk: views.post_edit(request, pk=pk, post_type=NEWS), name='news_edit'),
    path('<int:pk>/delete/', lambda request, pk: views.post_delete(request, pk=pk, post_type=NEWS), name='news_delete'),
    path('articles/create/', lambda request: views.post_create(request, post_type=ARTICLE), name='article_create'),
    path('articles/<int:pk>/edit/', lambda request, pk: views.post_edit(request, pk=pk, post_type=ARTICLE), name='article_edit'),
    path('articles/<int:pk>/delete/', lambda request, pk: views.post_delete(request, pk=pk, post_type=ARTICLE), name='article_delete'),

]