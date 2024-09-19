# Generated by Django 5.1.1 on 2024-09-19 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_emergency_photo_alter_problem_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergency',
            name='photo',
            field=models.ImageField(upload_to='emergency_photos/'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='user_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
