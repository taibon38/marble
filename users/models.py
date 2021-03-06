from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models.fields.files import ImageField
from django.contrib.auth.base_user import BaseUserManager
from app.models import Movie, Character
from django.db.models.signals import post_save  # receiverを利用するために記載（SNSログイン時にアバター取得目的）
from django.dispatch import receiver

# Create your models here.


class UserManager(BaseUserManager):
    """カスタムユーザーマネージャー"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # # emailを必須にする
        # if not email:
        #     raise ValueError('メールアドレスは必須です')
        # emailでUserモデルを作成FavedMovie
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
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
    username = models.CharField("ユーザー名", unique=True, blank=False, max_length=100)
    email = models.EmailField("メールアドレス")
    avatar = models.URLField("アイコン(SNSから取得)", max_length=200, blank=True)
    profile_icon = ImageField("アイコン", upload_to='profile_icons', blank=True, null=True)
    is_staff = models.BooleanField("is_staff", default=False)
    is_active = models.BooleanField("is_active", default=True)
    date_joined = models.DateTimeField("date_joined", default=timezone.now)
    faved_characters = models.ManyToManyField(
        Character,
        verbose_name='好きなキャラ',
        through="FavedCharacter",
        blank=True,
    )

    faved_movies = models.ManyToManyField(
        Movie,
        verbose_name='お気に入り映画',
        through="FavedMovie",
        blank=True,
        related_name='faved_users'  # 逆参照時の定義。movie.faved_usersでお気に入りしているユーザー一覧が取れる。ユーザーの数が取れるため、多い順などでとれる
    )

    watched_movies = models.ManyToManyField(
        Movie,
        verbose_name='閲覧済',
        through="WatchedMovie",
        blank=True,
        related_name='watched_movie'
    )

    objects = UserManager()
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']

    DEFAULT_PROFILE_ICON_PATH = 'images/user_icon.png'

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    # メールの送信に関するメソッド
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def profile_icon_url(self):
        if self.profile_icon:
            return self.profile_icon.url
        elif self.avatar:
            return self.avatar
        else:
            return staticfiles_storage.url(self.DEFAULT_PROFILE_ICON_PATH)


# お気に入り登録用のclass
class FavedCharacter(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class FavedMovie(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class WatchedMovie(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)