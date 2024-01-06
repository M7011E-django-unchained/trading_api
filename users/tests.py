from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class RegisterUserTest(APITestCase):
    """Test for the view RegisterUser."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:register')

    def test_create_user(self):
        """Test creating a new user."""
        payload = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)


class UpdateUserTest(APITestCase):
    """Test for the view UpdateUser."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        for user in User.objects.all():
            user.is_active = True
            user.save()
        self.url = reverse('users:update')

    def test_retrieve_user(self):
        """Test retrieving the profile for logged in user."""
        payload = {'username': 'testuser',
                   'password': 'testpass123'}
        response = self.client.post(
            reverse('users:token_obtain_pair'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        """Test updating the profile for logged in user."""
        payload = {'username': 'testuser',
                   'password': 'testpass123'}
        response = self.client.post(
            reverse('users:token_obtain_pair'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        payload = {'username': 'testuser',
                   'password': 'testpass123',
                   'email': 'newemail@test.com'
                   }

        response = self.client.patch(self.url, payload)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))


class CreateTokenTest(APITestCase):
    """Test for the view Token."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )
        for user in User.objects.all():
            user.is_active = True
            user.save()
        self.url = reverse('users:token_obtain_pair')

    def test_create_token(self):
        payload = {'username': 'testuser',
                   'password': 'testpass123'}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class RefreshTokenTest(APITestCase):
    """Test for the view Token."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )
        self.url = reverse('users:token_refresh')
        for user in User.objects.all():
            user.is_active = True
            user.save()

    def test_refresh_token(self):
        payload = {'username': 'testuser',
                   'password': 'testpass123'}
        response = self.client.post(
            reverse('users:token_obtain_pair'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['refresh']
        payload = {'refresh': token}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class VerifyTokenTest(APIClient):
    """Test for the view Token."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )
        self.url = reverse('users:token_verify')
        for user in User.objects.all():
            user.is_active = True
            user.save()

    def test_verify_token(self):
        payload = {'username': 'testuser',
                   'password': 'testpass123'}
        response = self.client.post(
            reverse('users:token_obtain_pair'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']
        payload = {'token': token}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
