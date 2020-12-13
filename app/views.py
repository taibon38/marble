from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

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
from .forms import (
    LoginForm, UserCreateForm, EmailChangeForm
)
from django.core.mail import BadHeaderError, send_mail  # 送信時のエラー解消目的
from .models import Category, Character, Movie, Character, MovieCharacter, MovieCategory


# お気に入り登録用で追加
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# フリーワード検索用で追加
from django.contrib import messages
from django.db.models import Q


# マイページの編集機能で追加
from django.views import generic
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

)
from django.urls import reverse_lazy
from django.contrib.auth import logout as auth_logout

# プロフィール情報編集で追加
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm
)

User = get_user_model()


# Create your views here.

def index(request):
    movies_list = Movie.objects.all().order_by('publication_date')
    characters_list = Character.objects.all()
    categories_list = Category.objects.all()

    """フリーワード検索機能の処理"""
    keyword = request.GET.get('keyword')

    if keyword:
        movies_list = movies_list.filter(
            Q(title__icontains=keyword) | Q(sumally__icontains=keyword) | Q(detail__icontains=keyword)
            # titleはMovieモデルのfield名、__icontains(部分一致)はQオブジェクトのプロパティ
        )
        messages.info(request, '「{}」の検索結果'.format(keyword))
    return render(request, 'app/index.html', {
        'movies_list': movies_list,
        'characters_list': characters_list,
        'categories_list': categories_list
        })


def privacy(request):
    return render(request, 'app/privacy.html')


def term(request):
    return render(request, 'app/term.html')


def search_category(request, category):
    # titleがURLの文字列と一致するCategoryインスタンスを取得
    category = get_object_or_404(Category, title=category)

    # 取得したCategoryに属する映画一覧を取得
    movies_list = Movie.objects.filter(categories=category)
    return render(request, 'app/index.html', {
        'search_theme':category,
        'category': category,
        'movies_list': movies_list
        })


def search_character(request, character):
    # titleがURLの文字列と一致するCharacterインスタンスを取得
    character = get_object_or_404(Character, name=character)
    # 取得したCharacterが属する映画一覧を取得
    movies_list = Movie.objects.filter(characters=character)

    return render(request, 'app/index.html', {
        'search_theme':character,
        'character': character,
        'movies_list': movies_list
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
        user.email_user(subject, message, settings.EMAIL_HOST_USER)
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


# マイページ関連

class Top(generic.TemplateView):
    template_name = 'index.html'


class ProfileView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        return render(self.request,'app/registration/profile.html')


class DeleteView(LoginRequiredMixin, generic.View):
    """退会機能"""
    def get(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        user.is_active = False  # 非アクティブになるだけで、データベースからは削除されない
        user.save()
        auth_logout(self.request)
        return render(self.request, 'app/registration/delete_complete.html')

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('app:password_change_done')
    template_name = 'app/registration/password_change_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'app/registration/password_change_done.html'


# プロフィール編集関連
# 参考サイト：https://blog.narito.ninja/detail/43#_2
class OnlyYouMixin(UserPassesTestMixin):  
    raise_exception = True # Falseならログインページに移動させる。

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのユーザー情報ページのpkが同じか、又はスーパーユーザーなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'app/user_detail.html'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """ユーザー編集"""
    model = User
    form_class = UserUpdateForm
    template_name = 'app/user_form.html'

    def get_success_url(self):
        return resolve_url('app:profile')

# パスワードリセット関連

class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'app/registration/password_reset_subject.txt'
    email_template_name = 'app/registration/password_reset_email.html'
    # email_template_name = 'app/registration/mail_template/password_reset/message.txt'
    template_name = 'app/registration/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('app:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'app/registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('app:password_reset_complete')
    template_name = 'app/registration/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'app/registration/password_reset_complete.html'


# メールアドレス再設定(参考：https://blog.narito.ninja/detail/136/)
class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'app/registration/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('app/registration/email_change_subject.txt', context)
        message = render_to_string('app/registration/email_change_message.txt', context)
        # send_mail(subject, message, None, [new_email])
        send_mail(subject, message, settings.EMAIL_HOST_USER, [new_email])

        return redirect('app:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'app/registration/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'app/registration/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)