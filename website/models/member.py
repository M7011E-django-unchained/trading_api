from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Member(models.Model):
    userid = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    profilePicPath = models.ImageField(
        upload_to="profile", null=True, blank=True)

    def __str__(self) -> str:
        return self.userid.username


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(userid=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.member.save()
