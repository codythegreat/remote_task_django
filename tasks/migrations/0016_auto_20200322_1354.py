# Generated by Django 3.0.4 on 2020-03-22 13:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0015_auto_20200322_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='team',
        ),
        migrations.AddField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='files',
            field=models.ManyToManyField(blank=True, to='tasks.FileAttachment'),
        ),
        migrations.AlterField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(blank=True, to='tasks.FileAttachment'),
        ),
    ]