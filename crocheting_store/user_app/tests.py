from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import StoreUser, EmailConfirmationToken
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


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


# class UserLoginTestCase(APITestCase):
   
#     def setUp(self):
#         self.user_data = {
#             'email': 'test@mail.com',
#             'password': 'testpassword',
#         }
#         self.user = StoreUser.objects.create(**self.user_data)
#         self.client = APIClient()
#         print(self.user)
#         print(self.user.password)

#     def test_loigin_api_view_is_working(self):
#         url = reverse ('login')
#         data = {'email': 'test@mail.com', 'password': 'testpassword'}
#         print(data)
#         response = self.client.post(url, data, format='json')
#         print(response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)


class UserEmailConfirmationTestCase(APITestCase):

    def test_user_information_view_requires_authentication(self):
        url = reverse('user_information_me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_send_email_confirmation_token_view_create_token(self):
    #     user = StoreUser.objects.create_user(
    #         email='test@mail.com',
    #         username='test_user',
    #         password='test_password'
    #     )
    #     self.client.force_authenticate(user=user)
    #     url = reverse('send_email_confirmation_token')
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     token = EmailConfirmationToken.objects.filter(user=user).first()
    #     self.assertIsNotNone(token)

    # def test_send_email_confirmation_token_view_requires_authentication(self):
    #     url = reverse('send_email_confirmation_token')
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LogoutViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_logout_success(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated(self):
        # Wylogowanie użytkownika
        self.client.logout()
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Token nie powinien zostać usunięty, ponieważ użytkownik jest nieuwierzytelniony
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_logout_no_token(self):
        # Usunięcie tokena przed próbą wylogowania
        self.token.delete()
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Token nie powinien zostać usunięty, ponieważ nie ma tokena
        self.assertFalse(Token.objects.filter(user=self.user).exists())
