# Generated by Django 5.1.5 on 2025-02-28 17:03

import utils.path_helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(blank=True, default='articles/default.png', null=True, upload_to=utils.path_helpers.article_cover_path, verbose_name='Обложка'),
        ),
    ]
