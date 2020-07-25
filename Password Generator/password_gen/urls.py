from django.urls import path
from password_gen.views import home_view, password_view


urlpatterns = [
    path('', home_view, name='home'),
    path('password/', password_view, name='password'),
]
