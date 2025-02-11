from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.TextField(max_length=255)
    title = models.TextField(max_length=255)
    text = models.TextField(max_length=65535)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)