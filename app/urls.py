from django.contrib import admin
from django.conf.urls import include, static
from .views import signup, toggle_fav_movies, faved_movies
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'app'
urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
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
]
