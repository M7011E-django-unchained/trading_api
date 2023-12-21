from django.contrib.auth.models import User
from website.models import Category, Subcategory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .helper import create_dummy_auctions, get_token


class SubcategoryListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="testuser",
        )
        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="staff",
            is_staff=True,
        )

    def test_get_subcategory(self):
        create_dummy_auctions()
        url = reverse("subcategory-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_subcategory(self):
        url = reverse("subcategory-list")
        Category.objects.create(name="Vehicle")

        payload = {"subcategory_name": "Train", "category": "Vehicle"}

        # user should not be allowed to create subcategories
        user_token = get_token(self.user, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Subcategory.objects.count(), 0)

        # staff should be allowed to create subcategories
        staff_token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subcategory.objects.count(), 1)
        self.assertEqual(Subcategory.objects.get().subcategory_name, "Train")

        # should not be possible to create duplicate subcategories
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Subcategory.objects.count(), 1)


class SubcategoryDetailTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testuser",
        )
        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="staff",
            is_staff=True,
        )
        create_dummy_auctions()

    def test_get_subcategory(self):
        url = reverse("subcategory-detail", args=["Car"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["subcategory_name"], "Car")

    def test_update_subcategory(self):

        url = reverse("subcategory-detail", args=["Car"])
        payload = {"subcategory_name": "Train",
                   "category": "Vehicle"}

        # user should not be allowed to update subcategories
        user_token = get_token(self.user, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")

        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        subcategories = Subcategory.objects.all()
        self.assertEqual(subcategories[0].subcategory_name, "Car")

        # staff should be allowed to update subcategories
        staff_token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")

        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subcategories = Subcategory.objects.all()
        self.assertEqual(subcategories[0].subcategory_name, "Train")

        # should not be possible to update subcategory to duplicate
        url = reverse("subcategory-detail", args=["Motorcycle"])
        payload = {"subcategory_name": "Train",
                   "category": "Vehicle"}
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        subcategories = Subcategory.objects.all()
        self.assertEqual(subcategories[0].subcategory_name, "Train")
        self.assertEqual(subcategories[1].subcategory_name, "Motorcycle")

    def test_delete_subcategory(self):
        url = reverse("subcategory-detail", args=["Car"])

        # user should not be allowed to delete subcategories
        user_token = get_token(self.user, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Subcategory.objects.count(), 3)

        # staff should be allowed to delete subcategories
        staff_token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {staff_token}")

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subcategory.objects.count(), 2)
        subcategories = Subcategory.objects.all()
        self.assertEqual(subcategories[0].subcategory_name, "Motorcycle")
        self.assertEqual(subcategories[1].subcategory_name, "Phone")
