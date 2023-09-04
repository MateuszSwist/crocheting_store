from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import StoreUserSerializer
from .models import EmailConfirmationToken, StoreUser

class CreateUserView(CreateAPIView):

    permission_classes = [AllowAny, ]
    serializer_class = StoreUserSerializer

class ListUsersView(ListAPIView):
    queryset = StoreUser.objects.all()
    serializer_class = StoreUserSerializer

class UserInformationView(APIView):

    permission_class = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        email = user.email
        is_email_acvite = user.ias_active
        payload = {'email': email, 'is_email_acvite': is_email_acvite}
        return Response(data=payload, status=status.HTTP_200_OK)
    
def send_confirmation_email(email, token_id, user_id):
    print('email send')

class SendEmailConfirmationTokenView(APIView):

    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        token = EmailConfirmationToken.objects.create(user=user)
        send_confirmation_email(
            email = user.email, 
            token_id=token.pk, 
            user_id=user.pk
            )
        return Response(data=None, status=status.HTTP_201_CREATED)


