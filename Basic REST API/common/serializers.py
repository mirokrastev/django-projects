from rest_framework import serializers

from common.models import List


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'title', 'content')
