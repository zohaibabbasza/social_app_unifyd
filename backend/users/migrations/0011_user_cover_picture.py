# Generated by Django 2.2.28 on 2023-02-20 22:09

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_profile_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cover_picture',
            field=models.ImageField(null=True, upload_to=core.utils.get_file_path),
        ),
    ]
