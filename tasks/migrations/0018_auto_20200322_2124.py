# Generated by Django 3.0.4 on 2020-03-22 21:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0017_auto_20200322_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ownedTeam', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='private',
            field=models.BooleanField(default=False),
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