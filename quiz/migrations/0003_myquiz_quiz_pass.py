# Generated by Django 4.2.11 on 2024-08-21 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_myquiz_duration_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='myquiz',
            name='quiz_pass',
            field=models.IntegerField(default=60, help_text="testdan o'tish foizi"),
        ),
    ]