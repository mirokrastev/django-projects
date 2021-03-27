from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urlshortener.api.serializers import URLSerializer
from urlshortener.common import generate_alias


class APICreateURL(APIView):
    authentication_classes = []

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = URLSerializer(data=self.request.data)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        url = form.validated_data['url']
        initial_alias = form.validated_data.get('alias', None)

        form.validated_data['alias'] = initial_alias or generate_alias(url)
        form.save()

        alias = form.validated_data['alias']

        return Response({'url': url, 'alias': alias}, status=status.HTTP_201_CREATED)

    def form_invalid(self, form):
        return Response({**form.errors}, status=status.HTTP_403_FORBIDDEN)
