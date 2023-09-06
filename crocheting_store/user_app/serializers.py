from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import request
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . models import StoreUser, EmailConfirmationToken
from . utils import send_confirmation_email


class StoreUserSerializer(serializers.ModelSerializer):

    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = StoreUser
        fields = [
            'email',
            'password',
            'password_confirmation'
        ]
        extra_kwargs = {
            'password':{
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data
    
    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return password

    def create(self, validate_data):
        user = StoreUser.objects.create_user(email=validate_data['email'], password=validate_data['password'])
        token = EmailConfirmationToken.objects.create(user=user)

        send_confirmation_email(
            email = user.email, 
            token_id=token.pk, 
            user_id=user.pk
            ) 
        return user        

class LoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

class ChangePasswordSerializer(serializers.Serializer):

    model = StoreUser

    old_password = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    
    confirm_new_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    def validate_new_password(self, new_password):
        validate_password(new_password)
        return new_password