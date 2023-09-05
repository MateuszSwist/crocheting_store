from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import StoreUser, EmailConfirmationToken


class UserCreateTestCase(APITestCase):

    def test_singup_api_view_is_working(self):
        url = reverse('create_user')
        data = {
            'email': 'test@mail.com',
            'username': 'test_user',
            'password': 'testpassword'
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

class UserEmailConfirmationTestCase(APITestCase):

    def test_send_email_confirmation_token_view_create_token(self):
        user = StoreUser.objects.create_user(
            email='test@mail.com',
            username='test_user',
            password='test_password'
        )
        self.client.force_authenticate(user=user)
        url = reverse('send_email_confirmation_token')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = EmailConfirmationToken.objects.filter(user=user).first()
        self.assertIsNotNone(token)

    def test_send_email_confirmation_token_view_requires_authentication(self):
        url = reverse('send_email_confirmation_token')
        response = self.client.post(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_information_view_requires_authentication(self):
        url = reverse('user_information_me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
