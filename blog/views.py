from django.shortcuts import render, get_object_or_404
from .models import BlogPost

# Create your views here.

def index(request):
    posts = BlogPost.objects.all()
    return render(request, "index.html", {"posts": posts})

def postdetails(request, postid):
    post = get_object_or_404(BlogPost, pk=postid)
    return render(request,"detail.html",{"post": post})