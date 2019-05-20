# Generated by Django 2.2.1 on 2019-05-18 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0008_auto_20190518_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=220)),
                ('swiss_specific', models.BooleanField(default=False)),
                ('weight', models.FloatField(blank=True, default=None, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
