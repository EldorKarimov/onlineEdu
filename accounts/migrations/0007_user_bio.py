# Generated by Django 4.2.11 on 2024-06-25 04:41

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='bio'),
        ),
    ]