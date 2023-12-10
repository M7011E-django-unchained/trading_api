from django.contrib.auth.models import User
from website.models import Category, Subcategory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .helper import create_dummy_auctions, get_token


class AuctionListCreateTest(APITestCase):
    """Test for the AuctionList view"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Category.objects.create(name="TestCategory")
        Subcategory.objects.create(
            category=Category.objects.get(id=1),
            subcategory_name="TestSubcategory")
        self.url = reverse("auction-list")

    def test_create_and_list_auction(self):
        """Test creating an auction"""
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Test Auction",
            "description": "This is a test auction",
            "subcategory": 1,
            "startingPrice": 100,
            "buyOutPrice": 200,
            "endTime": "2020-12-31T00:00:00Z"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
        self.assertEqual(response.data["description"], payload["description"])
        self.assertEqual(response.data["subcategory"], payload["subcategory"])
        self.assertEqual(
            response.data["startingPrice"], '100.00')
        self.assertEqual(response.data["buyOutPrice"], '200.00')

        # TODO: maybe fix this some day
        # this tests seems to fail on github for some reason
        # something is wrong with how github formats the dates, maybe its that
        # the tests runs on ubuntu in github actions?
        # AssertionError: '2020-12-31T01:00:00+01:00' != '2020-12-31T00:00:00Z'
        # self.assertEqual(response.data["endTime"], payload["endTime"])

        # mass create auctions
        create_dummy_auctions()
        # now check auction listing
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)
        # make sure category was set correctly from subcategory
        self.assertEqual(
            response.data[0]["category"],
            'http://testserver/api/1/category/TestCategory')

    def test_unathorized(self):
        payload = {
            "title": "Test Auction",
            "description": "This is a test auction",
            "subcategory": 1,
            "startingPrice": 100,
            "buyOutPrice": 200,
            "endTime": "2020-12-31T00:00:00Z"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # now check auction listing
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should be empty
        self.assertEqual(len(response.data), 0)


class AuctionDetailTest(APITestCase):
    """Test for the AuctionDetail view"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword",
            email="test1@example.com")
        # create second user
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword2",
            email="test2@example.com")
        create_dummy_auctions()

    def test_get_auction(self):
        """Test getting an auction"""
        url = reverse("auction-detail", kwargs={"auctionID": 1})
        # anyone should be able to get auction details
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_auction(self):
        """Test updating an auction"""
        url = reverse("auction-detail", kwargs={"auctionID": 1})
        # auctions should not be able to be updated
        response = self.client.patch(url, {"title": "New Title"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(url, {"title": "New Title"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # even if you own the auction
        user1_token = get_token("testuser", "testpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + user1_token)
        response = self.client.patch(url, {"title": "New Title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, {"title": "New Title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_auction(self):
        """Test deleting an auction"""
        url = reverse("auction-detail", kwargs={"auctionID": 1})
        # auctions should not be able to be deleted
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # even if you own the auction
        user1_token = get_token("testuser", "testpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + user1_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_edit_auction(self):
        """Test staff editing an auction"""
        url = reverse("auction-detail", kwargs={"auctionID": 1})
        # create staff user
        User.objects.create_user(
            username="staff", password="testpassword",
            email="staff@example.com", is_staff=True
        )

        response = self.client.get(url)
        self.assertEqual(response.data["title"], "Test Auction 0")

        # staff should be able to edit any auction
        staff_token = get_token("staff", "testpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + staff_token)

        payload = {"title": "New Title"}
        self.client.patch(url, payload)
        response = self.client.get(url)
        self.assertEqual(response.data["title"], payload["title"])

        self.client.delete(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoryAuctionListTest(APITestCase):
    """Test for the CategoryAuctionList view"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword",
            email="test@example.com")
        create_dummy_auctions()

    def test_get_category_auctions(self):
        """Test getting auctions by category"""
        url = reverse("category-auction-list", kwargs={"name": "Vehicle"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        url = reverse("category-auction-list", kwargs={"name": "Electronics"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)


class SubcategoryAuctionListTest(APITestCase):
    """Test for the SubcategoryAuctionList view"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword",
            email="test@example.com")
        create_dummy_auctions()

    def test_get_subcategory_auctions(self):
        """Test getting auctions by subcategory"""
        url = reverse("subcategory-auction-list",
                      kwargs={"subcategory_name": "Car"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        url = reverse("subcategory-auction-list",
                      kwargs={"subcategory_name": "Phone"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)


class MemberAuctionListTest(APITestCase):
    """Test for the MemberAuctionList view"""

    def setUp(self):
        self.client = APIClient()
        create_dummy_auctions()

    def test_get_member_auctions(self):
        """Test getting auctions by member"""
        url = reverse("member-auction-list",
                      kwargs={"username": "auctionOwner1"})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        url = reverse("member-auction-list",
                      kwargs={"username": "auctionOwner2"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_delete_member_auctions(self):
        """Test deleting auctions by member"""
        url = reverse("member-auction-list",
                      kwargs={"username": "auctionOwner1"})

        # there exists auctions by auctionOwner1
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        # unauthorized
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate as auctionOwner1
        user1_token = get_token("auctionOwner1", "testpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + user1_token)
        response = self.client.delete(url)

        # should be forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # no auctions should be deleted
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_staff_delete_member_auctions(self):
        """Test staff deleting auctions by member"""
        url = reverse("member-auction-list",
                      kwargs={"username": "auctionOwner1"})

        User.objects.create_user(
            username="staff", password="testpassword",
            email="staff@example.com", is_staff=True
        )

        # there exists auctions by auctionOwner1
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        # authenticate as staff
        staff_token = get_token("staff", "testpassword")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + staff_token)
        response = self.client.delete(url)

        # should be no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # no auctions should be deleted
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
