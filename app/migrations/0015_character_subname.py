# Generated by Django 3.1.3 on 2021-02-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_character_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='subname',
            field=models.CharField(default=1, max_length=150, verbose_name='サブネーム'),
            preserve_default=False,
        ),
    ]
