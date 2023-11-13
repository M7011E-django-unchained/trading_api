from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Member(models.Model):
    Username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    ProfilePicPath = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.Username.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(Username=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.member.save()


class Category(models.Model):
    CategoryId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=45, null=False, unique=True)

    def __str__(self) -> str:
        return self.Name


class Auction(models.Model):
    AuctionID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=45)
    AuctionOwner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # cascade = delete listing when user is deleted
    Description = models.CharField(max_length=255)
    ImagePath = models.CharField(max_length=45)
    Category = models.ManyToManyField(Category)
    StartingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    BuyOutPrice = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    StartTime = models.DateTimeField(
        auto_now_add=True  # set time to now when object is created
    )
    EndTime = models.DateTimeField()
    WinnerID = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="WinnerID",
    )
    Subscribed = models.ManyToManyField(User, related_name="SubscribedUser", blank=True)

    def __str__(self) -> str:
        return self.Title


class Shipment(models.Model):
    ShipmentID = models.AutoField(primary_key=True)
    Username = models.ForeignKey(User, on_delete=models.CASCADE)
    AuctionID = models.OneToOneField(Auction, null=True, on_delete=models.SET_NULL)
    BidAmount = models.DecimalField(max_digits=10, decimal_places=2)
    Paid = models.BooleanField(default=False)
    Shipped = models.BooleanField(default=False)
    ShippingDetails = models.CharField(max_length=255)
    Timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "AuctionID: " + str(self.ShipmentID)
