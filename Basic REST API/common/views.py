from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from common.models import List
from common.serializers import ListSerializer


class ListAPI(APIView):
    model = List
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        data = self.serializer_class(self.model.objects.all(), many=True)
        return Response(data.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)


class SingleListAPI(APIView):
    model = List
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        self.object = self.get_object(pk=pk, **kwargs)
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response(data=self.serializer_class(self.object).data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if not self.request.user == self.object.owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(instance=self.object, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        if not self.request.user == self.object.owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.object.delete()
        return Response(data=self.serializer_class(self.object).data, status=status.HTTP_200_OK)

    def get_object(self, pk, **kwargs):
        return self.model.objects.get(pk=pk, **kwargs)
