from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers import TagSerializer

from blog.models import Tag


@api_view(["GET"])
def tag_index(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response({"tags": serializer.data})


@api_view(["GET"])
def tag_detail(request, pk):
    tag = Tag.objects.get(pk=pk)
    serializer = TagSerializer(tag)
    return Response({"tag": serializer.data})


@api_view(["POST"])
def tag_create(request):
    data = request.data
    tag = Tag.objects.create(**data)
    serializer = TagSerializer(tag)
    return Response({"tag": serializer.data}, status=201)


@api_view(["PUT"])
def tag_update(request, pk):
    data = request.data
    tag = Tag.objects.get(pk=pk)
    tag.name = data["name"]
    tag.save()
    serializer = TagSerializer(tag)
    return Response({"tag": serializer.data})


@api_view(["DELETE"])
def tag_delete(request, pk):
    tag = Tag.objects.get(pk=pk)
    tag.delete()
    return Response({"message": "Tag deleted successfully!"})


@api_view(["GET"])
def tag_posts(request, pk):
    """Get all posts from a tag"""
    tag = Tag.objects.get(pk=pk)
    posts = tag.posts.all()
    serializer = TagSerializer(posts, many=True)
    return Response({"posts": serializer.data})
