from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:postid>', views.postdetails, name='post-details'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('new_post/', views.new_post, name='new-post'),
    path('post/<int:postid>/comment/', views.new_comment, name='new-comment'),
    path('post/<int:postid>/edit/', views.edit_post, name='edit-post'),
]
