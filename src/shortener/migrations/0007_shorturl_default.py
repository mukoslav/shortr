# Generated by Django 2.2.1 on 2019-05-18 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0006_auto_20190518_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='default',
            field=models.CharField(default='https://google.com', max_length=18),
        ),
    ]
