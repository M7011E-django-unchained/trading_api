from django.contrib.auth.models import User
from website.models import Category, Subcategory, Auction
from django.urls import reverse
from rest_framework.test import APIClient


def create_dummy_auctions():
    """Create dummy auctions for testing"""
    # make sure there are always 2 users
    User.objects.create_user(
        username="auctionOwner1", password="testpassword",
        email="auctionOwner1@example.com")
    User.objects.create_user(
        username="auctionOwner2", password="testpassword",
        email="auctionOwner2@example.com")
    for user in User.objects.all():
        user.is_active = True
        user.save()
    Category.objects.create(name="Vehicle")
    Subcategory.objects.create(
        category=Category.objects.get(id=1),
        subcategory_name="Car")
    Subcategory.objects.create(
        category=Category.objects.get(id=1),
        subcategory_name="Motorcycle")
    Category.objects.create(name="Electronics")
    Subcategory.objects.create(category=Category.objects.get(id=2),
                               subcategory_name="Phone")
    for i in range(5):
        Auction.objects.create(
            auctionOwner=User.objects.get(id=1),
            title="Test Auction " + str(i),
            description="This is a test auction " + str(i),
            category=Category.objects.get(id=1),
            subcategory=Subcategory.objects.get(id=1),
            startingPrice=100 + i,
            buyOutPrice=200 + i,
            endTime="2020-12-31T01:00:00+01:00",
        )
    for i in range(5):
        Auction.objects.create(
            auctionOwner=User.objects.get(id=2),
            title="Test Auction " + str(i),
            description="This is a test auction " + str(i),
            category=Category.objects.get(id=2),
            subcategory=Subcategory.objects.get(id=3),
            startingPrice=100 + i,
            buyOutPrice=200 + i,
            endTime="2020-12-31T01:00:00+01:00",
        )


def get_token(username, password):
    """Get token for user"""
    client = APIClient()
    url = reverse("users:token_obtain_pair")
    payload = {"username": username, "password": password}
    response = client.post(url, payload)
    return response.data["access"]
