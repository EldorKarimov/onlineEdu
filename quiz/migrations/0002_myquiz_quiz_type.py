# Generated by Django 4.2.11 on 2025-05-25 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myquiz',
            name='quiz_type',
            field=models.CharField(choices=[(1, 'Pre-course assessment'), (2, 'Midterm Exam'), (3, 'Final Exam'), (4, 'Lesson')], default=4, max_length=1),
        ),
    ]
