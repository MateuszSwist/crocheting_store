from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.http import request
from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import PasswordResetCompleteView

from .serializers import StoreUserSerializer, ChangePasswordSerializer, LoginSerializer
from .models import EmailConfirmationToken, StoreUser


class CreateUserView(CreateAPIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = StoreUserSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "User logged out successfully"})


class ListUsersView(ListAPIView):
    queryset = StoreUser.objects.all()
    serializer_class = StoreUserSerializer


class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        email = user.email
        is_email_acvite = user.is_email_confirmed
        payload = {"email": email, "is_email_acvite": is_email_acvite}
        return Response(data=payload, status=status.HTTP_200_OK)

def confirm_email_view(request):
    token_id = request.GET.get("token_id", None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        data = {"is_confirmed": True}
        return render(
            request, template_name="confirmation_mail_view.html", context=data
        )

    except EmailConfirmationToken.DoesNotExist:
        data = {"is_confirmed": False}
        return render(
            request, template_name="confirmation_mail_view.html", context=data
        )    

class ChangePasswordView(UpdateAPIView):

    def update(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            new_password_confirmation = serializer.validated_data.get(
                "confirm_new_password"
            )

            if not user.check_password(old_password):
                return Response(
                    "wrong old password", status=status.HTTP_400_BAD_REQUEST
                )

            if new_password != new_password_confirmation:
                return Response(
                    "incorrect password confirmation",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            else:
                user.set_password(new_password)
                user.save()
                return Response("password changed", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def delete(self, request):
        user = self.request.user
        user.delete()

        return Response("User deleted", status=status.HTTP_200_OK)




