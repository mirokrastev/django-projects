from rest_framework import serializers
from urlshortener.models import URLModel


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLModel
        fields = '__all__'
