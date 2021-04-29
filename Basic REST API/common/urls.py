from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from common.views import ListAPI, SingleListAPI

urlpatterns = [
    path('', ListAPI.as_view(), name='show_lists'),
    path('<int:pk>', SingleListAPI.as_view(), name='single_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
