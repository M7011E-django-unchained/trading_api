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
            shippingDetails="address user1")

        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=False,
            shippingDetails="address user1")

        Shipment.objects.create(
            username=self.user2, auctionID=Auction.objects.
            get(auctionID=3), shipped=False, paid=False,
            shippingDetails="address user2")

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


class ShipmentDetailTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testuser",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
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
            shippingDetails="address user1")
        Shipment.objects.create(
            username=self.user2, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=False,
            shippingDetails="address user2")
        self.url = reverse("shipment-detail", kwargs={"pk": 1})

    def test_get_shipment_detail_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_shipment_detail_as_user(self):

        # this user owns the shipment, so it should appear
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # this user does not own the shipment, so it should not appear
        token = get_token(self.user2, "testuser2")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_shipment_detail_as_staff(self):
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_shipment_detail_as_guest(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_shipment_detail_as_user(self):
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_shipment_detail_as_staff(self):
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ShipmentPaidTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testuser",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
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
            get(auctionID=1), shipped=False, paid=True,
            shippingDetails="address user1")
        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=True,
            shippingDetails="address user1")
        self.url = reverse("shipment-paid")

    def test_get_shipment_paid_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_shipment_paid_as_user(self):

        # this user owns the shipment, so it should appear
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # this user has only unpaid auctions, there should appear 0
        token = get_token(self.user2, "testuser2")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_shipment_paid_as_staff(self):
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ShipmentUnpaidTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testuser",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
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
            shippingDetails="address user1")
        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=True,
            shippingDetails="address user1")
        self.url = reverse("shipment-unpaid")

    def test_get_shipment_paid_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_shipment_paid_as_user(self):

        # this user owns the shipment, so it should appear
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # this user has only unpaid auctions, there should appear 0
        token = get_token(self.user2, "testuser2")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_shipment_paid_as_staff(self):
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ShipmentShippedTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testuser",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
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
            get(auctionID=1), shipped=True, paid=False,
            shippingDetails="address user1")
        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=True,
            shippingDetails="address user1")
        self.url = reverse("shipment-shipped")

    def test_get_shipment_shipped_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_shipment_shipped_as_user(self):

        # this user owns the shipment, so it should appear
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # this user has only unpaid auctions, there should appear 0
        token = get_token(self.user2, "testuser2")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_shipment_shipped_as_staff(self):
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ShipmentUnshippedTest(APIClient):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testuser",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
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
            get(auctionID=1), shipped=True, paid=False,
            shippingDetails="address user1")
        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=True,
            shippingDetails="address user1")
        self.url = reverse("shipment-unshipped")

    def test_get_shipment_unshipped_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_shipment_unshipped_as_user(self):

        # this user owns the shipment, so it should appear
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # this user has only unpaid auctions, there should appear 0
        token = get_token(self.user2, "testuser2")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_shipment_unshipped_as_staff(self):
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ShipmentUserListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testuser",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
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
            get(auctionID=1), shipped=True, paid=False,
            shippingDetails="address user1")
        Shipment.objects.create(
            username=self.user1, auctionID=Auction.objects.
            get(auctionID=2), shipped=False, paid=True,
            shippingDetails="address user1")

        self.url = reverse("shipment-user", kwargs={"pk": 1})

    def test_get_user_shipments_as_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_shipments_as_user(self):

        # this user is not a staff, should not be able to use this endpoint
        token = get_token(self.user1, "testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_shipments_as_staff(self):
        token = get_token(self.staff, "staff")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
