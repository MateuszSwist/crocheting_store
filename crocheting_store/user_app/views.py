from rest_framework.generics import CreateAPIView
from .models import StoreUser
from .serializers import StoreUserSerializer
from rest_framework.permissions import AllowAny

class CreateUserView(CreateAPIView):

    serializer_class = StoreUserSerializer
    permission_classes = (AllowAny, )