# Generated by Django 2.2.1 on 2019-05-18 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0009_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='shorturl_id',
            field=models.IntegerField(default=0),
        ),
    ]
