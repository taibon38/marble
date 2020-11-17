from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Movie(models.Model):
    """映画作品"""
    title = models.CharField(verbose_name='作品名', max_length=200)
    publication_date = models.DateField(verbose_name='公開日', blank=True)
    screening_time = models.PositiveIntegerField(
        verbose_name='上映時間', blank=True)
    sumally = models.TextField(verbose_name='あらすじ', blank=True)
    detail = models.TextField(verbose_name='解説', blank=True)
    movie_icon = models.ImageField(
        verbose_name='作品アイコン',
        upload_to='movie-icons',
        null=True,
        blank=True)
    category = models.ManyToManyField(
        "Category",
        through="MovieCategory",
    )
    

    def __str__(self):
        return self.title


class Character(models.Model):
    """キャラクター"""
    name = models.CharField(verbose_name='キャラクター名', max_length=150)
    character_icon = models.ImageField(
        verbose_name="キャラクターアイコン",
        upload_to='character_icons',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """楽しみ方"""
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class MovieCategory(models.Model):
    movie = models.ForeignKey("Movie",on_delete=models.CASCADE)
    category = models.ForeignKey("Category",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) #作成時に更新
    updated_at = models.DateTimeField(auto_now=True) #保存時に更新

class MovieCharacter(models.Model):
    movie = models.ForeignKey("Movie",on_delete=models.CASCADE)
    character = models.ForeignKey("Character",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) #作成時に更新
    updated_at = models.DateTimeField(auto_now=True) #保存時に更新