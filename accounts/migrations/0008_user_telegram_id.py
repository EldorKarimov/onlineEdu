# Generated by Django 4.2.11 on 2024-07-08 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(default=11223321, max_length=15, unique=True, verbose_name='telegram id'),
            preserve_default=False,
        ),
    ]