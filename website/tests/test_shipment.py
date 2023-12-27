from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from website.models import Shipment, Auction
from .helper import create_dummy_auctions, get_token


class ShipmentListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testuser",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="testuser2",
        )
        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="staff",
            is_staff=True,
        )
        create_dummy_auctions()
        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=1), shipped=False, paid=False,
            bidAmount=1000, shippingDetails="address user1")

        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=False,
            bidAmount=1000, shippingDetails="address user1")

        Shipment.objects.create(
            username=self.user2, auctionID=Auction.objects.
            get(auctionID=3), shipped=False, paid=False,
            bidAmount=1000, shippingDetails="address user2")

    def test_get_shipment_as_guest(self):
        url = reverse("shipment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_shipment_as_user(self):
        url = reverse("shipment-list")

        # this user owns the shipment, so it should appear
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # this user does not own any shipments, so only 1 should appear
        token = get_token(self.user2, "testuser2")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_shipment_as_staff(self):
        url = reverse("shipment-list")
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
