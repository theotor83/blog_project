from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/p<int:postid>-<slug:slug>/', views.postdetails, name='post-details'),
    path('post/<int:postid>/', views.postdetails_old, name='post-details-old'), #deprecated
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('new_post/', views.new_post, name='new-post'),
    path('post/<int:postid>/comment/', views.new_comment, name='new-comment'),
    path('post/<int:postid>/edit/', views.edit_post, name='edit-post'),
    path('profile/<int:userid>/', views.profile_page, name='profile-page'),
    path('profile/<int:userid>/edit', views.edit_profile, name='edit-profile'),
    path('like-post/<int:post_id>/', views.like_post, name='like-post'),
    path('dislike-post/<int:post_id>/', views.dislike_post, name='dislike-post'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like-comment'),
    path('dislike-comment/<int:comment_id>/', views.dislike_comment, name='dislike-comment'),
    path('post/<int:postid>/delete/', views.delete_post, name='delete-post'),
    path('post/<int:postid>/delete-comment/<int:commentid>', views.delete_comment, name='delete-comment'),
    path('search', views.search, name='search'),
]
    