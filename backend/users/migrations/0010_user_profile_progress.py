# Generated by Django 2.2.28 on 2023-02-20 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20230217_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_progress',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
