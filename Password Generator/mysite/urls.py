"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.password_gen, name='password_gen')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='password_gen')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('password_gen/', include('password_gen.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from password_gen.views import about_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('password_gen.urls')),
    path('about/', about_view, name='about')
]
