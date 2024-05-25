from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers import CategorySerializer, PostSerializer

from blog.models import Category


@api_view(["GET"])
def category_index(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response({"categories": serializer.data})


@api_view(["GET"])
def category_detail(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response({"category": serializer.data})


@api_view(["POST"])
def category_create(request):
    data = request.data
    category = Category.objects.create(**data)
    serializer = CategorySerializer(category)
    return Response({"category": serializer.data}, status=201)


@api_view(["PUT"])
def category_update(request, pk):
    data = request.data
    category = Category.objects.get(pk=pk)
    category.name = data["name"]
    category.save()
    serializer = CategorySerializer(category)
    return Response({"category": serializer.data})


@api_view(["DELETE"])
def category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return Response({"message": "Category deleted successfully!"})


@api_view(["GET"])
def category_posts(request, pk):
    """Get all posts from a category"""
    category = Category.objects.get(pk=pk)
    posts = category.post_set.all()
    serializer = PostSerializer(posts, many=True)
    return Response({"posts": serializer.data})
