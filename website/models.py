from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Member(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    profilePicPath = models.ImageField(
        upload_to="profile", null=True, blank=True)

    def __str__(self) -> str:
        return self.userid.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(userid=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.member.save()


class Category(models.Model):
    name = models.SlugField(
        max_length=45, null=False, unique=True, blank=False, allow_unicode=True
    )

    def __str__(self) -> str:
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="parent_category"
    )
    subcategory_name = models.SlugField(
        max_length=45,
        null=False,
        unique=True,
        blank=False,
        allow_unicode=True,
    )

    def __str__(self) -> str:
        return self.subcategory_name


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
