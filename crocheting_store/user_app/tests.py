from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from .models import(StoreUser, 
                    EmailConfirmationToken)
from .utils import send_confirmation_email
from .views import confirm_email_view


class UserCreateTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('create_user')
        self.data = {
            'email': 'test@mail.com',
            'password': 'testpassword',
            'password_confirmation': 'testpassword'
        }

    def test_singup_api_view_is_working(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = StoreUser.objects.filter(email=self.data['email']).first()
        self.assertIsNotNone(created_user)
        self.assertTrue(created_user.check_password('testpassword'))

    def test_differece_password_case(self):
        self.data['password_confirmation'] = 'testpassword1'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                
    def test_no_double_email(self):
        response = self.client.post(self.url, self.data, format='json')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginViewTests(APITestCase):

    def setUp(self):
        self.email = 'test@mail.com'
        self.password = 'testpassword'
        self.user = StoreUser.objects.create_user(email=self.email, password=self.password)

    def test_login_valid_user(self):
        url = reverse('login')
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_user(self):
        url = reverse('login')
        data = {'email': self.email, 'password': 'invalid_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'error': 'Invalid credentials'})

    def test_login_missing_username(self):
        url = reverse('login')
        data = {'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_password(self):
        url = reverse('login')
        data = {'email': self.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

class EmailConfirmationTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = StoreUser.objects.create_user(
            email='test@example.com',
            password='testpassword',
        )
        self.token = EmailConfirmationToken.objects.create(user=self.user)
        self.expected_link = f'confirm_email?token_id={self.token.pk}&user_id={self.user.pk}'

    def test_sending_confrimation_link(self):
        email = 'test@example.com'
        send_confirmation_email(email, self.token.id, self.user.id)
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]    
        self.assertIn(self.expected_link, sent_mail.body)

    def test_starting_cofnrimation_view(self):
        url = reverse('confirm_email') + f'?token_id={self.token.id}&user_id={self.user.id}'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = confirm_email_view(request)
        self.assertEqual(response.status_code, 200)

class ChangePasswordViewTestCase(APITestCase):

    def setUp(self):
        self.user = StoreUser.objects.create_user(
            email='test@user.com',
            password='testpassword'
        )
        self.url = reverse('change_password')

    def test_change_password(self):
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword123',
            'confirm_new_password': 'newpassword123',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_change_password_incorrect_old_password(self):
        data = {
            'old_password': 'incorrect_password',
            'new_password': 'newpassword123',
            'confirm_new_password': 'newpassword123',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_incorrect_confirmation(self):
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword123',
            'confirm_new_password': 'different_password',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_unauthenticated(self):
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword123',
            'confirm_new_password': 'newpassword123',
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)