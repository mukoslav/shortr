# Generated by Django 2.2.1 on 2019-05-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_auto_20190517_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='shorturl',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
