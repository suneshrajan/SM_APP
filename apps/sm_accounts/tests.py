from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, ValidateEmail
from rest_framework.authtoken.models import Token
from utils.helpers import get_hashed_otp


class UserSignupTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('user-signup') 

    def test_user_signup(self):
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'image': 'testimage.jpg',
        }
        response = self.client.post(self.signup_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('data', response.data)
        self.assertIn('detail', response.data)

        # Additional assertions for the created user and associated models
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Token.objects.filter(user__username='testuser').exists())
        self.assertTrue(ValidateEmail.objects.filter(user__username='testuser').exists())

    def test_user_signup_existing_email(self):
        User.objects.create(username='existinguser', email='test@example.com', password='testpassword')
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(self.signup_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A user with that email already exists.', response.data['detail'])

    def test_user_signup_invalid_data(self):
        payload = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password': '',
        }
        response = self.client.post(self.signup_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)  # Assert that the error message includes 'email'
        self.assertIn('password', response.data)  # Assert that the error message includes 'password'


class UserLoginTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user-login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.verification = ValidateEmail.objects.create(user=self.user)

    def test_user_login(self):
        payload = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.login_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('data', response.data)
        self.assertIn('detail', response.data)

    def test_user_login_invalid_credentials(self):
        payload = {
            'username': self.username,
            'password': 'invalidpassword',
        }
        response = self.client.post(self.login_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "missing user")

    def test_user_login_unverified_email(self):
        self.verification.is_verified = False
        self.verification.save()
        payload = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.login_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('data', response.data)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'User email is not verified, please verify your email.')


class UserLogoutTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('user-logout')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_logout(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Successful logout")

    def test_user_logout_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GenerateOTPTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.generate_otp_url = reverse('generate-otp') 
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_generate_otp(self):
        response = self.client.get(self.generate_otp_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

    def test_generate_otp_email_verified(self):
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)
        response = self.client.get(self.generate_otp_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'User email already verified.')


class VerifyOTPTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.verify_otp_url = reverse('verify-otp') 
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.otp = get_hashed_otp('1234')
        self.validate_email_obj = ValidateEmail.objects.create(user_id=self.user.id, otp=self.otp)

    def test_verify_otp_success(self):
        payload = {
            'otp': '1234',
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.verify_otp_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_email_obj.refresh_from_db()
        self.assertTrue(self.validate_email_obj.is_verified)

    def test_verify_otp_invalid_otp(self):
        payload = {
            'otp': '5678',
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.verify_otp_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['detail'] == 'Please enter valid otp')
        self.validate_email_obj.refresh_from_db()
        self.assertFalse(self.validate_email_obj.is_verified)

    def test_verify_otp_user_already_verified(self):
        self.validate_email_obj.is_verified = True
        self.validate_email_obj.is_active = True
        self.validate_email_obj.save()

        payload = {
            'otp': '1234',
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.verify_otp_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['detail'] == 'User already verified.')

    def test_verify_otp_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        payload = {
            'otp': '1234',
        }
        response = self.client.post(self.verify_otp_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_otp_exception(self):
        payload = {
            'otp': '1234',
        }
        self.client.force_login(user=self.user)
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_accounts.views.get_hashed_otp') as mocked_hashed_otp:
            mocked_hashed_otp.side_effect = Exception('Something went wrong')
            response = self.client.post(self.verify_otp_url, payload)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))

