# Generated by Django 2.2.28 on 2023-03-06 16:49

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20230303_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.get_file_path),
        ),
    ]
