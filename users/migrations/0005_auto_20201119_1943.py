# Generated by Django 3.1.3 on 2020-11-19 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201119_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='メールアドレス'),
        ),
    ]
