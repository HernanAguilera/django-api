from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers import PostSerializer

from blog.models import Post


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
    post.title = data["title"]
    post.content = data["content"]
    post.save()
    serializer = PostSerializer(post)
    return Response({"post": serializer.data})


@api_view(["DELETE"])
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return Response({"message": "Post deleted successfully!"})
