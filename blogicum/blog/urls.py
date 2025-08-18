from django.urls import path

from . import views

app_name = 'blog'

#: Список маршрутов приложения 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('location/<slug:slug>/', views.location_posts, name='location_posts'),
]
