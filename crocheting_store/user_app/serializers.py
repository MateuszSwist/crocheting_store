from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import request

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . models import StoreUser



class StoreUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreUser
        fields = [
            'email',
            'password',
        ]
        extra_kwargs = {
            'password':{
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
        
    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return password

    def create(self, validate_data):
        user = StoreUser.objects.create_user(email=validate_data['email'], password=validate_data['password'])

        return user        


