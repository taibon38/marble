from django.db import models
from django.contrib.auth.models import PermissionsMixin 
from django.contrib.auth.base_user import AbstractBaseUser 
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models.fields.files import ImageField
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    """カスタムユーザーマネージャー"""

    use_in_migrations = True

    def _create_user(self,email,password,**extra_fields):
        #emailを必須にする
        if not email:
            raise ValueError('メールアドレスは必須です')
        #emailでUserモデルを作成
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields): 
        extra_fields.setdefault('is_staff', False) 
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields): 
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True') 
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True') 
        return self._create_user(email, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin): 
    """カスタムユーザーモデル"""
    name = models.TextField("ユーザー名",blank=False,max_length=100)
    email = models.EmailField("メールアドレス",unique=True)
    profile_icon = ImageField("プロフィールアイコン",upload_to='profile_icons')
    is_staff = models.BooleanField("is_staff", default=False) 
    is_active = models.BooleanField("is_active", default=True)
    date_joined = models.DateTimeField("date_joined",default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = "email" 
    EMAIL_FIELD = "email" 
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user" 
        verbose_name_plural = "users"

    # メールの送信に関するメソッド
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)