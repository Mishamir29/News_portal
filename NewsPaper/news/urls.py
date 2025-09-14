from django.urls import path
from . import views
from .views import NewsList, NewsDetail, PostDeleteView, PostCreate, CategoryDetail, user_profile

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

    # path('category/<int:pk>/subscribe/', views.subs, name= 'subs'),

    path('category/<int:pk>/', CategoryDetail.as_view(), name= 'category_detail'),

    path('profile/', user_profile, name='user_profile'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('category/<int:pk>/subscribe/', views.subscribe_category, name='subscribe_category'),
    path('category/<int:pk>/unsubscribe/', views.unsubscribe_category, name='unsubscribe_category'),



]