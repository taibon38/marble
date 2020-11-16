from django.db import DefaultConnectionProxy, models
from django.contrib.auth import get_user_model

# Create your models here.
class Movie(models.Model):
    """映画作品"""
    title = models.CharField(verbose_name='作品名',max_length=200) 
    publication_date = models.DateField(verbose_name='公開日',blank=True) 
    screening_time = models.PositiveIntegerField(verbose_name='上映時間',blank=True) 
    sumally = models.TextField(verbose_name='あらすじ',blank=True) 
    detail = models.TextField(verbose_name='解説',blank=True) 
    movie_icon = models.ImageField(verbose_name='作品アイコン',upload_to='movie-icons',null=True,blank=True) 
    
    def __str__(self):
        return self.title