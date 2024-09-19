# Generated by Django 5.1.1 on 2024-09-19 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_danger_level_ai_problem_priority_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authority',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='authority',
            name='website',
        ),
        migrations.AddField(
            model_name='ai_problem',
            name='subdivision',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='authority',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
