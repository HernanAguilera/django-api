from .views import posts

from django.urls import path
from django.urls.conf import include

app_name = "blog"

urlpatterns = [
    path(
        "posts/",
        include(
            [
                path("", posts.index, name="posts.index"),
                path("<int:pk>/", posts.post_detail, name="posts.detail"),
                path("create/", posts.post_create, name="posts.create"),
                path("<int:pk>/update/", posts.post_update, name="posts.update"),
                path("<int:pk>/delete/", posts.post_delete, name="posts.delete"),
            ]
        ),
        name="posts",
    ),
    path(
        "comments/",
        include(
            [
                path("<int:pk>/", posts.post_comments, name="comments"),
                path("<int:pk>/create/", posts.comment_create, name="comments.create"),
                path("<int:pk>/update/", posts.comment_update, name="comments.update"),
                path("<int:pk>/delete/", posts.comment_delete, name="comments.delete"),
            ]
        ),
        name="comments",
    ),
]
