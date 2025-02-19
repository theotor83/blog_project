from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='blog_posts')
    image = models.ImageField(default='placeholder.jpg', blank=True)
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, blank=True)
    text = models.TextField(max_length=65535)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.TextField(max_length=4096)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"By {self.user.username} : {self.text[:100]}"
    
    @property
    def getParentPostId(self):
        print(self.post.id)
        return self.post.id
    

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_count = models.IntegerField(default=-1)
    comment_count = models.IntegerField(default=-1)
    bio = models.TextField(null=True, blank=True, max_length=255)
    profile_picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"Profile {self.user.username}"

    @property
    def get_post_count(self):
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
    
    def get_recent_activity(self, limit=5):
        posts = BlogPost.objects.filter(user=self.user).order_by('-dateCreated')[:limit]
        comments = Comment.objects.filter(user=self.user).order_by('-dateCreated')[:limit]
        
        activities = []
        for post in posts:
            activities.append({
                'type': 'post',
                'date': post.dateCreated,
                'title': post.title,
                'preview': post.text[:100],
                'id': post.id,
            })
        
        for comment in comments:
            activities.append({
                'type': 'comment',
                'date': comment.dateCreated,
                'title': comment.post.title,
                'preview': comment.text[:100],
                'id': comment.post.id,
            })
        
        return sorted(activities, key=lambda x: x['date'], reverse=True)[:limit]