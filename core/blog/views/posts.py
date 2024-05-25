from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers import PostSerializer, CommentSerializer

from blog.models import Post, Comment


def is_post_owner(user, post):
    return user == post.user


def is_comment_owner(user, comment):
    return user == comment.user


@api_view(["GET"])
def index(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({"posts": serializer.data})


@api_view(["GET"])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    serializer = PostSerializer(post)
    return Response({"post": serializer.data})


@api_view(["POST"])
def post_create(request):
    data = {**request.data, "user_id": request.user.id}
    tags = data.pop("tags") if "tags" in data else []
    post = Post.objects.create(**data)
    if tags:
        post.tags.set(tags)
    serializer = PostSerializer(post)
    return Response({"post": serializer.data})


@api_view(["PUT"])
def post_update(request, pk):
    data = request.data
    post = Post.objects.get(pk=pk)
    if not is_post_owner(request.user, post):
        return Response({"message": "You are not the owner of this post!"}, status=403)
    post.title = data["title"]
    post.content = data["content"]
    post.save()
    serializer = PostSerializer(post)
    return Response({"post": serializer.data})


@api_view(["DELETE"])
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if not is_post_owner(request.user, post):
        return Response({"message": "You are not the owner of this post!"}, status=403)
    post.delete()
    return Response({"message": "Post deleted successfully!"})


@api_view(["GET"])
def post_comments(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comments.all()
    return Response({"comments": CommentSerializer(comments, many=True).data})


@api_view(["POST"])
def comment_create(request, pk):
    post = Post.objects.get(pk=pk)
    data = {**request.data, "user_id": request.user.id, "post_id": post.id}
    comment = Comment.objects.create(**data)
    serializer = CommentSerializer(comment)
    return Response({"comment": serializer.data})


@api_view(["PUT"])
def comment_update(request, pk):
    data = request.data
    comment = Comment.objects.get(pk=pk)
    if not is_comment_owner(request.user, comment):
        return Response(
            {"message": "You are not the owner of this comment!"}, status=403
        )
    comment.body = data["body"]
    comment.save()
    serializer = CommentSerializer(comment)
    return Response({"comment": serializer.data})


@api_view(["DELETE"])
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    if not is_comment_owner(request.user, comment):
        return Response(
            {"message": "You are not the owner of this comment!"}, status=403
        )
    comment.delete()
    return Response({"message": "Comment deleted successfully!"})
