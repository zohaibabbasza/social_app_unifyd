# Generated by Django 2.2.28 on 2023-03-24 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_cover_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='category',
        ),
        migrations.RemoveField(
            model_name='group',
            name='group_privacy',
        ),
    ]
