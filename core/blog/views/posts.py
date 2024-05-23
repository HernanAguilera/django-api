
from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import Post

@api_view(['GET'])
def index(request):
    posts = Post.objects.all()
    return Response({'posts': posts})


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return Response({'post': post})


@api_view(['POST'])
def post_create(request):
    data = request.data
    post = Post.objects.create(**data)
    return Response({'post': post})


@api_view(['PUT'])
def post_update(request, pk):
    data = request.data
    post = Post.objects.get(pk=pk)
    post.title = data['title']
    post.content = data['content']
    post.save()
    return Response({'post': post})


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return Response({'message': 'Post deleted successfully!'})