from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
# Create your views here.


class RegisterUser(CreateAPIView):
    serializer_class = UserSerializer
