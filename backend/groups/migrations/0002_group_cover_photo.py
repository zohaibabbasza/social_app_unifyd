# Generated by Django 2.2.28 on 2023-03-23 13:43

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.get_file_path),
        ),
    ]