# Generated by Django 2.2.1 on 2019-05-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_shorturl_short_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shorturl',
            name='short_url',
            field=models.CharField(max_length=21, unique=True),
        ),
    ]
