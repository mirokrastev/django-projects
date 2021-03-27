from django.urls import path, include
from urlshortener.views import CreateURL, RedirectURL

urlpatterns = [
    path('create/', CreateURL.as_view(), name='create'),
    path('<path:alias>/', RedirectURL.as_view(), name='redirect'),

    # API urlconf
    path('api', include('urlshortener.api.urls'))
]
