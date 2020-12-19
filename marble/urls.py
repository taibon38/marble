"""marble URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.urls import path
from django.contrib.auth import views as auth_views
from app import views
from django.conf import settings #ImageFieldの画像表示目的
from django.conf.urls.static import static #ImageFieldの画像表示目的
from app.views import handle_page_not_found

urlpatterns = [
    path('cockpit/', admin.site.urls),  # adminのURLを自由に指定
    path('',include('app.urls')),
    path('oauth/',include('social_django.urls',namespace='social')),
    path('accounts/profile/',views.index,name='index'),
]

handler404 = handle_page_not_found

# 画像表示目的で追加
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)