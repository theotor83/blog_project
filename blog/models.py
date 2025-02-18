from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='blog_posts')
    image = models.ImageField(default='placeholder.jpg', blank=True)
    title = models.CharField(max_length=255, null=True)
    text = models.TextField(max_length=65535)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.TextField(max_length=4096)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"By {self.user.username} : {self.text[:100]}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_count = models.IntegerField(default=-1)
    comment_count = models.IntegerField(default=-1)

    @property
    def get_post_count(self):
        print(self.post_count)
        if self.post_count == -1:
            self.post_count = self.user.blog_posts.count()
            self.save()
        return self.post_count
        
    @property
    def get_comment_count(self):
        if self.comment_count == -1:
            self.comment_count = self.user.comments.count()
            self.save()
        return self.comment_count