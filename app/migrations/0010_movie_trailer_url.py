# Generated by Django 3.1.3 on 2020-12-27 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201126_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_url',
            field=models.URLField(blank=True, verbose_name='予告編'),
        ),
    ]