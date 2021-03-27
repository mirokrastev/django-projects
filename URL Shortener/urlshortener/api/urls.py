from django.urls import path
from urlshortener.api.views import APICreateURL

urlpatterns = [
    path('', APICreateURL.as_view()),
]
