from django.urls import path
from . import views
from .views import NewsList, NewsDetail, PostDeleteView, PostCreate, upgrade_me

urlpatterns = [
    path('', NewsList.as_view(), name= 'post_list'),

    path('<int:pk>/',NewsDetail.as_view(), name= 'news_detail'),

    path('search/',views.news_search, name='news_search'),

    path('news/create/',PostCreate.as_view(), name='news_create'),

    path('news/<int:pk>/edit/',views.PostUpdate.as_view(), name='news_edit'),

    path('news/<int:pk>/delete/',PostDeleteView.as_view(), name='news_delete'),

    path('articles/create/',views.PostCreate.as_view(), name='article_create'),

    path('articles/<int:pk>/edit/',views.PostUpdate.as_view(), name='article_edit'),

    path('articles/<int:pk>/delete/',PostDeleteView.as_view(), name='article_delete'),

    path('protected/', views.protected_view, name='protected'),

    path('upgrade/', views.upgrade_me, name= 'upgrade_me'),

]