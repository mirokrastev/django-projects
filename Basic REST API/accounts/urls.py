from django.urls import path
from accounts.views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='api-register'),
    path('token-auth', LoginAPIView.as_view(), name='api-token-auth'),
]
