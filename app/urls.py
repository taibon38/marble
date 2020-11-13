from django.contrib import admin
from django.conf.urls import include
from app.views import signup
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'app' 
urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/',views.signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='app/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

