
from .views import posts

from django.urls import path
app_name = 'blog'

urlpatterns = [
    path('posts/', posts.index, name='posts.index'),
    path('posts/<int:pk>/', posts.post_detail, name='posts.detail'),
    path('posts/create/', posts.post_create, name='posts.create'),
    path('posts/<int:pk>/update/', posts.post_update, name='posts.update'),
    path('posts/<int:pk>/delete/', posts.post_delete, name='posts.delete'),
]