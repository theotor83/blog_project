# Generated by Django 5.1.6 on 2025-02-16 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_image_name_alter_blogpost_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image_name',
            field=models.ImageField(blank=True, default='template.png', upload_to=''),
        ),
    ]
