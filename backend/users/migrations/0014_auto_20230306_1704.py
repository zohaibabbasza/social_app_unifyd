# Generated by Django 2.2.28 on 2023-03-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='display_name_as',
        ),
        migrations.AddField(
            model_name='preference',
            name='is_date_of_birth',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='preference',
            name='is_location',
            field=models.BooleanField(default=True),
        ),
    ]
