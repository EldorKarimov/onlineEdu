# Generated by Django 4.2.11 on 2024-08-22 09:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userlessonprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlessonprogress',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userlessonprogress',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
