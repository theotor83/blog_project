from django.contrib import admin
from . import models

admin.site.register(models.BlogPost)
admin.site.register(models.Comment)
admin.site.register(models.Profile)