# Generated by Django 3.1.3 on 2020-11-16 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_icon',
            field=models.ImageField(upload_to='profile_icons', verbose_name='プロフィールアイコン'),
        ),
    ]
