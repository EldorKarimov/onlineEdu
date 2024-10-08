# Generated by Django 4.2.11 on 2024-08-22 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_course_slug_lesson_slug_module_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLessonProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False, verbose_name='completed')),
                ('is_open', models.BooleanField(default=False, verbose_name='open')),
                ('course', models.ManyToManyField(to='main.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.lesson', verbose_name='lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'unique_together': {('user', 'lesson')},
            },
        ),
    ]
