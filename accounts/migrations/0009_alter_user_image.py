# Generated by Django 4.2.11 on 2024-07-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='/home/hacktivist/projects/onlineEdu/static/assets/images/teacher/teacher__1.png', null=True, upload_to='media/users/', verbose_name='Image'),
        ),
    ]
