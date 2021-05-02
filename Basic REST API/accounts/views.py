from rest_framework.views import APIView
from accounts.serializers import UserSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class RegisterAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        # Check signals.py for generate_token signal that
        # creates a token for this user

        token = Token.objects.get(user=user)
        # Querying the created token from generate_token function in signals.py

        return Response(data={'token': str(token)}, status=status.HTTP_201_CREATED)


LoginAPIView = ObtainAuthToken
