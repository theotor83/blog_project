# Generated by Django 5.1.6 on 2025-02-18 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_profile_bio_profile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
    ]
