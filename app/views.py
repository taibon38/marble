from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.shortcuts import render

# メール認証機能用で追加
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm
)
from django.core.mail import BadHeaderError  # 送信時のエラー解消目的
from .models import Category, Character, Movie 

# お気に入り登録用で追加
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Character, MovieCharacter

User = get_user_model()


# Create your views here.

def index(request):
    movies_list = Movie.objects.all().order_by('publication_date')
    characters_list = Character.objects.all()
    categories_list = Category.objects.all()
    return render(request, 'app/index.html', {
        'movies_list': movies_list ,
        'characters_list': characters_list,
        'categories_list': categories_list
        })


def mypage(request):
    user = request.user
    faved_movies_list = user.faved_movies.all()
    watched_movies_list = user.watched_movies.all()
    faved_characters_list = user.faved_characters.all()
    return render(request, 'app/mypage.html', {
        'faved_movies_list': faved_movies_list,
        'watched_movies_list': watched_movies_list,
        'faved_characters_list': faved_characters_list
        })


def character(request, pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, 'app/character.html', {'character': character})


def movie_character(request, movie_character):
    movie_character = MovieCharacter.objects.get(name=movie_character)
    return render(request, 'app/character.html', {'movie_character': movie_character})
def movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'app/movie.html', {'movie': movie})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(email=input_email, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

# お気に入りの映画登録
# お気に入りボタンの作成(ユーザーの状態によって表示を切り替える)
@login_required
@require_POST
def toggle_fav_movies(request):
    fav_movie = get_object_or_404(Movie, pk=request.POST["movie_id"])
    user = request.user
    if fav_movie in user.faved_movies.all():
        user.faved_movies.remove(fav_movie)
    else:
        user.faved_movies.add(fav_movie)
    return redirect('app:movie', pk=fav_movie.id)

# お気に入り結果の表示
@login_required
def faved_movies(request):
    user = request.user
    movies = user.faved_movies.all()
    return render(request, 'app/mypage.html', {'movies': movies})


# 観たよボタンの作成
@login_required
@require_POST
def toggle_watch_movies(request):
    watch_movie = get_object_or_404(Movie, pk=request.POST["movie_id"])
    user = request.user
    if watch_movie in user.watched_movies.all():
        user.watched_movies.remove(watch_movie)
    else:
        user.watched_movies.add(watch_movie)
    return redirect('app:movie', pk=watch_movie.id)

# 観たよの表示
@login_required
def watched_movies(request):
    user = request.user
    movies = user.watched_movies.all()
    return render(request, 'app/mypage.html', {'movies': movies})


# 好きボタンの作成
@login_required
@require_POST
def toggle_fav_characters(request):
    fav_character = get_object_or_404(Character, pk=request.POST["character_id"])
    user = request.user
    if fav_character in user.faved_characters.all():
        user.faved_characters.remove(fav_character)
    else:
        user.faved_characters.add(fav_character)
    return redirect('app:character', pk=fav_character.id)

# 好き結果の表示
@login_required
def faved_characters(request):
    user = request.user
    characters = user.faved_characters.all()
    return render(request, 'app/mypage.html', {'characters': characters})



# メール認証時に追加
class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'app/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string(
            'app/mail_template/create/subject.txt',
            context).strip()  # .strip()で改行を取り除く
        message = render_to_string(
            'app/mail_template/create/message.txt',
            context).strip()

        # 宛先１名に対する送信メソッド。user.email_user('メールの件名', 'メールの本文')
        user.email_user(subject, message)
        return redirect('app:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'app/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'app/user_create_complete.html'
    timeout_seconds = getattr(
        settings,
        'ACTIVATION_TIMEOUT_SECONDS',
        60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignaturxeExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()
