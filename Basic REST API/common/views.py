from rest_framework.response import Response
from rest_framework import permissions, status, generics
from common.models import List
from common.serializers import ListSerializer


class ListAPI(generics.GenericAPIView):
    serializer_class = ListSerializer
    queryset = List.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SingleListAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer
    queryset = List.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs): return self.check_owner()

    def delete(self, request, *args, **kwargs): return self.check_owner()

    def check_owner(self, *args, **kwargs):
        instance = self.get_object()
        if not instance.owner == self.request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().put(self.request, *args, **kwargs)
