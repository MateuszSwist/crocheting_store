from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import(StoreUser, 
                    EmailConfirmationToken)
from .views import confirm_email_view


class UserCreateTestCase(APITestCase):

    def test_singup_api_view_is_working(self):
        url = reverse('create_user')
        data = {
            'email': 'test@mail.com',
            'username': 'test_user',
            'password': 'testpassword',
            'password_confirmation': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = StoreUser.objects.filter(email=data['email']).first()
        self.assertIsNotNone(created_user)
        self.assertTrue(created_user.check_password('testpassword'))

    def test_no_double_email(self):
        url = reverse('create_user')
        data = {
            'email': 'test@mail.com',
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserInformationTestCase(APITestCase):

    def test_user_information_view_requires_authentication(self):
        url = reverse('user_information_me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_information_view_data_is_working(self):
        self.user = StoreUser.objects.create_user(
            email='test@mail.com',
            password='test_password'
        )
        self.client.force_authenticate(user=self.user) 
        url = reverse('user_information_me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['is_email_acvite'], self.user.is_email_confirmed)


class LogoutViewTestCase(APITestCase):
    def test_logout_success(self):        
        self.user = StoreUser.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

# class EmailConfirmationTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = get_user_model().objects.create_user(
#             email='test@example.com',
#             password='testpassword',
#             is_email_confirmed=False
#         )
#         self.token = EmailConfirmationToken.objects.create(user=self.user)

#     def test_email_confirmation_successful(self):
#         url = reverse('confirm_email')
#         request = self.factory.get(url, {'token_id': self.token.pk})
#         response = confirm_email_view(request)

#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.context['is_confirmed'])
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.is_email_confirmed)

#     def test_email_confirmation_token_does_not_exist(self):
#         url = reverse('confirm_email')
#         request = self.factory.get(url, {'token_id': 'nonexistent_token_id'})
#         response = confirm_email_view(request)

#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(response.context['is_confirmed'])
#         self.user.refresh_from_db()
#         self.assertFalse(self.user.is_email_confirmed)
