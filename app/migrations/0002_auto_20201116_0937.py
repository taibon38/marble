# Generated by Django 3.1.3 on 2020-11-16 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=200, verbose_name='作品名'),
        ),
    ]
