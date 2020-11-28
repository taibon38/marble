# Generated by Django 3.1.3 on 2020-11-16 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201116_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='detail',
            field=models.TextField(blank=True, verbose_name='解説'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_icon',
            field=models.ImageField(blank=True, null=True, upload_to='movie-icons', verbose_name='作品アイコン'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='publication_date',
            field=models.DateField(blank=True, verbose_name='公開日'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='screening_time',
            field=models.PositiveIntegerField(blank=True, verbose_name='上映時間'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='sumally',
            field=models.TextField(blank=True, verbose_name='あらすじ'),
        ),
    ]
