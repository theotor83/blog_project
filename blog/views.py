from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from . import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    posts = BlogPost.objects.all().select_related('user').order_by('-id')
    return render(request, "index.html", {"posts": posts})

def postdetails_old(request, postid):
    post = get_object_or_404(BlogPost, pk=postid)
    return redirect('post-details', postid=post.id, slug=post.slug)

def postdetails(request, postid, slug):
    post = get_object_or_404(BlogPost, pk=postid)
    comments = Comment.objects.filter(post=post)
    form = forms.CommentForm()

    if post.slug != slug:
        return redirect('post-details', postid=post.id, slug=post.slug)

    return render(request, "detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required()
def new_post(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()

            # Update post_count in Profile
            profile = request.user.profile
            profile.post_count += 1
            profile.save()

            return redirect('index')
    else:
        form = forms.PostForm()
    return render(request, 'new_post.html', {'form': form})

@login_required
def new_comment(request, postid):
    post = get_object_or_404(BlogPost, pk=postid)

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  # Ensure the user is logged in
            comment.save()

            # Update comment_count in Profile
            profile = request.user.profile
            profile.comment_count += 1
            profile.save()
            
            return redirect('post-details', postid=post.id, slug=post.slug)

    return redirect('post-details', postid=post.id, slug=post.slug)

@login_required
def edit_post(request, postid):
    post = get_object_or_404(BlogPost, id=postid)

    if request.user != post.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.dateUpdated = timezone.now()
            post.save()
            return redirect('post-details', postid=post.id)
    else:
        form = forms.PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form})

def profile_page(request, userid):
    user = get_object_or_404(User, pk=userid)
    profile, created = Profile.objects.get_or_create(user=user)
    profile.get_post_count
    profile.get_comment_count

    recent = profile.get_recent_activity()

    return render(request, 'profile_page.html', {'requested_user':user, 'recent':recent})


@login_required
def edit_profile(request, userid):
    user = get_object_or_404(User, id=userid)
    profile = get_object_or_404(Profile, id=userid)

    if request.user != profile.user and request.user.is_superuser == False:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            #profile.dateUpdated = timezone.now()
            profile.save()
            return redirect('profile-page', userid=userid)
    else:
        form = forms.ProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form, 'requested_user':user})



def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    author = get_object_or_404(User, id=post.user.id)

    if user in post.dislikes.all():
        post.dislikes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation += 1
            author.profile.save()

    if user in post.likes.all():
        post.likes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation -= 1
            author.profile.save()
    else:
        post.likes.add(user)
        if author.profile.reputation != None:
            author.profile.reputation += 1
            author.profile.save()

    return JsonResponse({
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count()
    })


def dislike_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    author = get_object_or_404(User, id=post.user.id)

    if user in post.likes.all():
        post.likes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation -= 1
            author.profile.save()
    
    if user in post.dislikes.all():
        post.dislikes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation += 1
            author.profile.save()
    else:
        post.dislikes.add(user)
        if author.profile.reputation != None:
            author.profile.reputation -= 1
            author.profile.save()

    

    return JsonResponse({
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count()
    })



def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    author = get_object_or_404(User, id=comment.user.id)

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation += 1
            author.profile.save()
        

    if user in comment.likes.all():
        comment.likes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation -= 1
            author.profile.save()

    else:
        comment.likes.add(user)
        if author.profile.reputation != None:
            author.profile.reputation += 1
            author.profile.save()

    return JsonResponse({
        'likes_count': comment.likes.count(),
        'dislikes_count': comment.dislikes.count()
    })

def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    author = get_object_or_404(User, id=comment.user.id)

    if user in comment.likes.all():
        comment.likes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation -= 1
            author.profile.save()
            
    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
        if author.profile.reputation != None:
            author.profile.reputation += 1
            author.profile.save()

    else:
        comment.dislikes.add(user)
        if author.profile.reputation != None:
            author.profile.reputation -= 1
            author.profile.save()

    return JsonResponse({
        'likes_count': comment.likes.count(),
        'dislikes_count': comment.dislikes.count()
    })