# Generated by Django 3.1.3 on 2020-12-28 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20201227_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='introduction',
            field=models.TextField(blank=True, verbose_name='説明文'),
        ),
    ]