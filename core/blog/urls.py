from .views import posts, categories, tags

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
    path(
        "categories/",
        include(
            [
                path("", categories.category_index, name="categories.index"),
                path("<int:pk>/", categories.category_detail, name="categories.detail"),
                path("create/", categories.category_create, name="categories.create"),
                path(
                    "<int:pk>/update/",
                    categories.category_update,
                    name="categories.update",
                ),
                path(
                    "<int:pk>/delete/",
                    categories.category_delete,
                    name="categories.delete",
                ),
                path(
                    "<int:pk>/posts/",
                    categories.category_posts,
                    name="categories.posts",
                ),
            ]
        ),
        name="categories",
    ),
    path(
        "tags/",
        include(
            [
                path("", tags.tag_index, name="tags.index"),
                path("<int:pk>/", tags.tag_detail, name="tags.detail"),
                path("create/", tags.tag_create, name="tags.create"),
                path("<int:pk>/update/", tags.tag_update, name="tags.update"),
                path("<int:pk>/delete/", tags.tag_delete, name="tags.delete"),
                path("<int:pk>/posts/", tags.tag_posts, name="tags.posts"),
            ]
        ),
        name="tags",
    ),
]
