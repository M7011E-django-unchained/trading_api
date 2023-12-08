from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class RegisterUser(CreateAPIView):
    serializer_class = UserSerializer


class UpdateUser(RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
