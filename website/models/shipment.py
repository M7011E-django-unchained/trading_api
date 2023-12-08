from django.db import models
from django.contrib.auth.models import User
from .auction import Auction


class Shipment(models.Model):
    shipmentID = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    auctionID = models.OneToOneField(
        Auction, null=True, on_delete=models.SET_NULL)
    bidAmount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    shippingDetails = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "AuctionID: " + str(self.shipmentID)
