from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.sm_accounts.models import ValidateEmail
from .models import User, UserFollower
from rest_framework.authtoken.models import Token


class UserProfileViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_prsonal_profile_url = reverse('user-personal-profile')
        self.user = User.objects.create_user(username='testuser', password='testpassword', email="test@testmail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)

    def test_get_user_profile_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.user_prsonal_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get(self.user_prsonal_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile_exception(self):
        self.client.force_login(self.user)
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_users.views.User.objects.get') as mocked_get:
            mocked_get.side_effect = Exception('Something went wrong')
            response = self.client.get(self.user_prsonal_profile_url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))


class UserSearchViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.search_user_url = reverse('search-user')
        self.user = User.objects.create_user(username='testuser', password='testpass', first_name='John', last_name='Doe')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)

    def test_search_users_success(self):
        self.client.force_login(self.user)
        response = self.client.get(f'{self.search_user_url}?search=John')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_users_empty_query(self):
        self.client.force_login(self.user)
        response = self.client.get(f'{self.search_user_url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_users_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get(f'{self.search_user_url}?search=John')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_users_exception(self):
        self.client.force_login(self.user)
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_users.views.User.objects.filter') as mocked_filter:
            mocked_filter.side_effect = Exception('Something went wrong')
            response = self.client.get(f'{self.search_user_url}?search=John')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))


class UserFollowerViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.another_user = User.objects.create_user(username='followeruser', password='followerpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.search_user_url = f'/api/users/user/'
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)

    def test_follow_user_success(self):
        self.client.force_login(self.user)
        response = self.client.post(f'{self.search_user_url}{self.user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_follow_user_already_following(self):
        user_folliwer_obj = UserFollower.objects.create(user=self.user)
        user_folliwer_obj.followers.add(self.another_user)
        self.client.force_login(self.user)
        response = self.client.post(f'{self.search_user_url}{self.another_user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_user_follower_not_found(self):
        self.client.force_login(self.user)
        response = self.client.post(f'{self.search_user_url}{999}/follow/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_user_success(self):
        user_folliwer_obj = UserFollower.objects.create(user=self.user)
        user_folliwer_obj.followers.add(self.another_user)
        self.client.force_login(self.user)
        response = self.client.delete(f'{self.search_user_url}{self.another_user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_user_not_following(self):
        self.client.force_login(self.user)
        response = self.client.delete(f'{self.search_user_url}{self.user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_user_follower_not_found(self):
        self.client.force_login(self.user)
        response = self.client.delete(f'{self.search_user_url}{999}/follow/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_user_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.post(f'{self.search_user_url}{self.another_user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollow_user_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.delete(f'{self.search_user_url}{self.another_user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_user_exception(self):
        self.client.force_login(self.user)
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_users.views.User.objects.filter') as mocked_filter:
            mocked_filter.side_effect = Exception('Something went wrong')
            response = self.client.post(f'{self.search_user_url}{self.another_user.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))

