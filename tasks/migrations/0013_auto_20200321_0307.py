# Generated by Django 3.0.4 on 2020-03-21 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_auto_20200320_2030'),
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
