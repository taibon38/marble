# Generated by Django 3.1.3 on 2020-11-17 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_category_character'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.ManyToManyField(through='app.MovieCategory', to='app.Category'),
        ),
    ]