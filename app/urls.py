from django.contrib import admin
from django.conf.urls import include, static
from .views import signup, toggle_fav_movies, faved_movies
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


app_name = 'app'
urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
    path(
        'privacy/',
        views.privacy,
        name='privacy'),
    path(
        'term/',
        views.term,
        name='term'),
    path(
        'how/',
        views.how,
        name='how'),
    path(
        'contact/',
        views.contact,
        name='contact'),
    path(
        'mypage/',
        views.mypage,
        name='mypage'),
    path(
        'signup/',
        views.signup,
        name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='app/login.html'),
        name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'),
    path(
        'user_create/',
        views.UserCreate.as_view(),
        name='user_create'),
    path(
        'user_create/done',
        views.UserCreateDone.as_view(),
        name='user_create_done'),
    path(
        'user_create/complete/<token>/',
        views.UserCreateComplete.as_view(),
        name='user_create_complete'),
    path(
        'character/<int:pk>',
        views.character,
        name='character'),
    path(
        'movie_character/<str:movie_character>/', 
        views.movie_character,  
        name='movie_character'
        ),
    path(
        'movie/<int:pk>',
        views.movie,
        name='movie'),
    path(
        'toggle_fav_movies/',
        views.toggle_fav_movies,
        name='toggle_fav_movies'),
    path(
        'faved_movies/', 
        views.faved_movies, 
        name='faved_movies'),
    path(
        'toggle_watch_movies/',
        views.toggle_watch_movies,
        name='toggle_watch_movies'),
    path(
        'watched_movies/', 
        views.watched_movies, 
        name='fwatched_movies'),
    path(
        'toggle_fav_characters/',
        views.toggle_fav_characters,
        name='toggle_fav_characters'),
    path(
        'faved_characters/', 
        views.faved_characters, 
        name='faved_characters'),
    path(
        'search/categories/<str:category>/', 
        views.search_category,
        name='search_category'),  # index.htmlで楽しみ方タグで検索できる機能
    path(
        'search/characters/<str:character>/', 
        views.search_character,
        name='search_character'),  # index.htmlでキャラクター名タグで検索できる機能
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('delete_confirm', TemplateView.as_view(template_name='app/registration/delete_confirm.html'), name='delete-confirmation'),
    path('delete_complete', views.DeleteView.as_view(), name='delete-complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
]

handler404 = 'app.views.handle_page_not_found'