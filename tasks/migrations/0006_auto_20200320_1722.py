# Generated by Django 3.0.4 on 2020-03-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20200320_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completeData',
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