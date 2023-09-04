from rest_framework import serializers, permissions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from . models import StoreUser



class StoreUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreUser
        fields = [
            'email',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validate_data):
        user = StoreUser.objects.create_user(email=validate_data['email'], password=validate_data['password'])
        return user        


# class StoreUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = StoreUser
#         fields = [
#             'email',
#             'password', 
#             'username', 
#             ]
        
#         extra_kwargs = {
#             'password':{
#                 'write_only': True,
#                 'style': {'input_type': 'password'}
#             }
#         }
        
#     def validate_password(self, password):
#         try:
#             validate_password(password)
#         except ValidationError as e:
#             raise serializers.ValidationError(e.messages)
#         return password
    
#     def create(self, validated_data):
#         user = StoreUser.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )

#         StoreUser.set_password(user, validated_data['password'])

#         return user
    

