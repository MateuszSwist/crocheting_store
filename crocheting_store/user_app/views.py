from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


from rest_framework.authtoken.models import Token

from django.http import request
from django.shortcuts import render


from .serializers import StoreUserSerializer
from .models import EmailConfirmationToken, StoreUser
from .utils import send_confirmation_email

class CreateUserView(CreateAPIView):

    permission_classes = [AllowAny, ]
    serializer_class = StoreUserSerializer

class ListUsersView(ListAPIView):
    queryset = StoreUser.objects.all()
    serializer_class = StoreUserSerializer
class UserInformationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        email = user.email
        is_email_acvite = user.is_email_confirmed
        payload = {'email': email, 'is_email_acvite': is_email_acvite}
        return Response(data=payload, status=status.HTTP_200_OK)
    
def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        data = {'is_confirmed': True}
        return render(
            request,
            template_name='confirmation_mail_view.html',
              context=data
              )
                    
    except EmailConfirmationToken.DoesNotExist:
        data = {'is_confirmed': False}
        return render(
            request,
            template_name='confirmation_mail_view.html',
              context=data
              )