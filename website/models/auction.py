from django.db import models
from django.contrib.auth.models import User
from .category import Category
from .subcategory import Subcategory


class Auction(models.Model):
    auctionID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    auctionOwner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # cascade = delete listing when user is deleted
    description = models.CharField(max_length=255)
    imagePath = models.ImageField(upload_to="profile", null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, null=True)
    startingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    buyOutPrice = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    startTime = models.DateTimeField(
        auto_now_add=True  # set time to now when object is created
    )
    endTime = models.DateTimeField()
    winnerID = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="WinnerID",
    )
    subscribed = models.ManyToManyField(
        User, related_name="SubscribedUser", blank=True)

    def __str__(self) -> str:
        return self.title
