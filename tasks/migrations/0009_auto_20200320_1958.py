# Generated by Django 3.0.4 on 2020-03-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_auto_20200320_1953'),
    ]

    operations = [
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
