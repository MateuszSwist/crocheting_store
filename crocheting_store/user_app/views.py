from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from smtplib import SMTPException

from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import request
from django.shortcuts import render

from .serializers import StoreUserSerializer
from .models import EmailConfirmationToken, StoreUser

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
    
def send_confirmation_email(email, token_id, user_id):
    data = {
        'token_id': str(token_id),
        'user_id': str(user_id)
    }
    message = get_template('confirmation.txt').render(data)
    try:
        send_mail(
            subject="Please confirm email", 
            message=message,
            from_email=None,
            recipient_list=[email],
            fail_silently=True
            )
    except SMTPException as e: (f' {e} Problem with mail confirmation, contact with crochetingstorewro@gmail.com')


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    # user_id = request.GET.get('user_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        print(user)
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
                                                   
class SendEmailConfirmationTokenView(APIView):

    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        try:
            token = EmailConfirmationToken.objects.get(user=user)
            token.delete()
        except EmailConfirmationToken.DoesNotExist:
            print('stworzylem nowy token')
            pass

        token = EmailConfirmationToken.objects.create(user=user)
        send_confirmation_email(
            email = user.email, 
            token_id=token.pk, 
            user_id=user.pk
            )
        return Response(data=None, status=status.HTTP_201_CREATED)

