from django.contrib.auth.models import User
from website.models import Category
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .helper import create_dummy_auctions, get_token


class CategoryListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = User.objects.create_user(
            username="staff", password="staff",
            email="staff@example.com", is_staff=True)
        self.user = User.objects.create_user(
            username="user", password="user", email="user@example.com")
        for user in User.objects.all():
            user.is_active = True
            user.save()

    def test_create_category(self):
        url = reverse("category-list")
        payload = {"name": "test"}

        # user should not be allowed to create categories
        user_token = get_token(self.user, "user")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 0)

        # staff should be allowed to create categories
        staff_token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "test")

        # should not be possible to create duplicate categories
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 1)

    def test_list_categories(self):
        url = reverse("category-list")
        create_dummy_auctions()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class CategoryDetailTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = User.objects.create_user(
            username="staff", password="staff",
            email="staff@example.com", is_staff=True)
        self.user = User.objects.create_user(
            username="user", password="user", email="user@example.com")
        Category.objects.create(name="test")
        for user in User.objects.all():
            user.is_active = True
            user.save()

    def test_get_category(self):
        url = reverse("category-detail", args=["test"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test")

    def test_update_category(self):
        url = reverse("category-detail", args=["test"])
        payload = {"name": "test2"}

        # user should not be allowed to update categories
        user_token = get_token(self.user, "user")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.get().name, "test")

        # staff should be allowed to update categories
        staff_token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get().name, "test2")

        # should not be possible to update to duplicate category
        Category.objects.create(name="test")
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, "test2")
        self.assertEqual(categories[1].name, "test")

    def test_delete_category(self):
        url = reverse("category-detail", args=["test"])

        # user should not be allowed to delete categories
        user_token = get_token(self.user, "user")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 1)

        # staff should be allowed to delete categories
        staff_token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
