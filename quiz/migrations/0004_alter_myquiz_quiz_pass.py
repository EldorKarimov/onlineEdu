# Generated by Django 4.2.11 on 2024-08-21 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_myquiz_quiz_pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myquiz',
            name='quiz_pass',
            field=models.FloatField(default=60, help_text="testdan o'tish foizi"),
        ),
    ]
