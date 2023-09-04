from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import StoreUser, EmailConfirmationToken


class UserEmailConfirmationTestCase(TestCase):
    def setUp(self):
        self.user = StoreUser.objects.create_user(
            email='test@mail.com',
            username = 'test_user',
            password = 'test_password'
        )

    def test_user_information_view_requires_authentication(self):
        url = reverse('user_information_me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_email_confirmation_token_view_requires_authentication(self):
        url = reverse('send_email_confirmation_token')
        respones = self.client.post(url)
        self.assertEqual(respones.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_email_confirmation_token_view_create_token(self):
        user = self.user
        url = reverse('send_email_confirmation_token')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = EmailConfirmationToken.objects.filter(user=user).first()
        self.assertIsNone(token)
