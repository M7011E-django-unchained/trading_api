from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from .helper import get_token


class TestMemberList(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword2",
            email="test2@example.com",
        )
        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword3",
            email="test3@example.com",
        )
        self.staff = User.objects.create_user(
            username="staff",
            password="staffpassword",
            email="staff@example.com",
            is_staff=True,
        )

        self.url = reverse("member-list")

    def test_get_member_list_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_member_list_as_user(self):
        token = get_token(self.user, "testpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_member_list_as_staff(self):
        token = get_token(self.staff, "staffpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class TestMemberDetail(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        self.staff = User.objects.create_user(
            username="staff",
            password="staffpassword",
            email="staff@example.com",
            is_staff=True,
        )

        self.url = reverse("member-detail", kwargs={"username": "testuser"})

    def test_get_member_detail_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # a member should use the edit user endpoint instead of this endpoint.
    # This is for member management
    def test_get_member_detail_as_user(self):
        token = get_token(self.user, "testpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_member_detail_as_staff(self):
        token = get_token(self.staff, "staffpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_update_member_detail_as_staff(self):
        token = get_token(self.staff, "staffpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "new@example.com",
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "new@example.com")
