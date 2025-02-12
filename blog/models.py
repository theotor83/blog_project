from django.db import models
from django.utils import timezone

# Create your models here.
class BlogPost(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.TextField(max_length=255)
    title = models.PositiveIntegerField(null=True)
    text = models.TextField(max_length=65535)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(default=timezone.now)