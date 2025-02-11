from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def index(request):
    posts = BlogPost.objects.all()
    return render(request, "index.html")

def post_details(request, post_id):
    post = get_object_or_404(BlogPost, pk=id)
    return render(request, "detail.html", {'post':post})

