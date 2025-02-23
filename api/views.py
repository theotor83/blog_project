from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import BlogPost
from .serializers import PostSerializer

# Create your views here.

@api_view(['GET'])
def get_all_posts(request):
    posts = BlogPost.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)