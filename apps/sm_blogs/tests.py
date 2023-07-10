from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.sm_accounts.models import ValidateEmail
from .models import LikePost, User, UserPost
from rest_framework.authtoken.models import Token


class UserBlogTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_blog_url = reverse('user-blog')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)

    def test_get_user_posts_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.user_blog_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user_post_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.force_login(self.user)
        payload = {
            'content': 'Test content',
        }
        response = self.client.post(self.user_blog_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_user_post_missing_content(self):
        self.client.force_login(self.user)
        payload = {
            'title': 'Test title',
        }
        response = self.client.post(self.user_blog_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_posts_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get(self.user_blog_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_user_post_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        data = {
            'content': 'Test content',
        }
        response = self.client.post(self.user_blog_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_user_post_exception(self):
        self.client.force_login(self.user)
        data = {
            'content': 'Test content',
        }
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_blogs.views.UserPostSerializers') as mocked_serializer:
            mocked_serializer.side_effect = Exception('Something went wrong')
            response = self.client.post(self.user_blog_url, data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))


class FollowerBlogTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.follower_blog_url = reverse('follower-blog')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)

    def test_get_follower_posts_success(self):
        self.client.force_login(self.user)
        response = self.client.get(self.follower_blog_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_follower_posts_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get(self.follower_blog_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_follower_posts_exception(self):
        self.client.force_login(self.user)
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_blogs.views.UserFollower.objects.filter') as mocked_filter:
            mocked_filter.side_effect = Exception('Something went wrong')
            response = self.client.get(self.follower_blog_url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))


class LikeBlogTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_post = UserPost.objects.create(content='Test content', user=self.user)
        self.like_unlike_blog_url = f'/api/blogs/user/following/'
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)

    def test_like_post_success(self):
        self.client.force_login(self.user)
        response = self.client.get(f'{self.like_unlike_blog_url}{self.user_post.id}/post/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_post_already_liked(self):
        LikePost.objects.create(user=self.user, post=self.user_post)
        self.client.force_login(self.user)
        response = self.client.get(f'{self.like_unlike_blog_url}{self.user_post.id}/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_post_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(f'{self.like_unlike_blog_url}{999}/post/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unlike_post_success(self):
        LikePost.objects.create(user=self.user, post=self.user_post)
        self.client.force_login(self.user)
        response = self.client.delete(f'{self.like_unlike_blog_url}{self.user_post.id}/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_post_not_found(self):
        self.client.force_login(self.user)
        response = self.client.delete(f'{self.like_unlike_blog_url}{999}/post/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unlike_post_not_liked(self):
        self.client.force_login(self.user)
        response = self.client.delete(f'{self.like_unlike_blog_url}{self.user_post.id}/post/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_post_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get(f'{self.like_unlike_blog_url}{self.user_post.id}/post/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unlike_post_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.delete(f'{self.like_unlike_blog_url}{self.user_post.id}/post/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_post_exception(self):
        self.client.force_login(self.user)
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_blogs.views.LikePost.objects.filter') as mocked_filter:
            mocked_filter.side_effect = Exception('Something went wrong')
            response = self.client.get(f'{self.like_unlike_blog_url}{self.user_post.id}/post/')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))


class CommentBlogTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_post = UserPost.objects.create(content='Test content', user=self.user)
        self.comment_blog_url = reverse('comment-blog')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        ValidateEmail.objects.create(user=self.user, is_verified=True, is_active=True)

    def test_add_comment_success(self):
        self.client.force_login(self.user)
        data = {
            'post_id': self.user_post.id,
            'comment': 'Test comment',
        }
        response = self.client.post(self.comment_blog_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_post_not_found(self):
        self.client.force_login(self.user)
        data = {
            'post_id': 999,  # Non-existing post ID
            'comment': 'Test comment',
        }
        response = self.client.post(self.comment_blog_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_comment_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        data = {
            'post_id': self.user_post.id,
            'comment': 'Test comment',
        }
        response = self.client.post(self.comment_blog_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_comment_exception(self):
        self.client.force_login(self.user)
        data = {
            'post_id': self.user_post.id,
            'comment': 'Test comment',
        }
        # Simulate an exception being raised during the view's execution
        with patch('apps.sm_blogs.views.CommentPost.objects.create') as mocked_create:
            mocked_create.side_effect = Exception('Something went wrong')
            response = self.client.post(self.comment_blog_url, data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue('Something went wrong' in str(response.data))

