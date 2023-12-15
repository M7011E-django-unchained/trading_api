from django.db import models
from django.contrib.auth.models import User
from .auction import Auction


class Subscription(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    auctionID = models.ForeignKey(Auction, on_delete=models.CASCADE,
                                  db_column='auctionID')

    class Meta:
        managed = False
        db_table = 'subscriptions'
        unique_together = (('userID', 'auctionID'),)
