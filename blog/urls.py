from django.urls import path
from .views import ArticleList, ArticleDetail, CategoryList

app_name='blog'
urlpatterns = [
    path('home', ArticleList.as_view(), name='home'),
    path('page/<int:page>', ArticleList.as_view(), name='home'),
    path('article/<slug:slug>', ArticleDetail.as_view(), name='detail'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category'),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name='category'),
    # path('home', home, name='home'),
    # path('page/<int:page>', home, name='home'),
    # path('article/<slug:slug>', detail, name='detail'),
    # path('category/<slug:slug>', category, name='category'),
    # path('category/<slug:slug>/page/<int:page>', category, name='category'),
    # path('home', home, name='home'),
    # path('api', api, name='api'),
    # path('article/<slug:slug>', detail, name='detail'),
]