# Generated by Django 2.2.1 on 2019-05-17 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postitapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='body',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='body',
            field=models.TextField(max_length=3000),
        ),
    ]
