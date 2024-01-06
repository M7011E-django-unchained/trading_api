from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
)
from django.contrib.auth.models import User
from website.models import Member


# Member/User serializers
class MemberDetailSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ("profilePicPath",)


class UserListSerializer(HyperlinkedModelSerializer):
    username = HyperlinkedIdentityField(
        view_name="member-detail",
        lookup_field="username",
    )

    class Meta:
        model = User
        fields = ("username",)


class UserDetailSerializer(ModelSerializer):
    profilePicPath = MemberDetailSerializer(
        source="member",
        read_only=True,
    )

    auctions = HyperlinkedIdentityField(
        view_name="member-auction-list",
        lookup_field="username",
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "profilePicPath",
            "auctions",
        )


class UserDetailLimitedSerializer(ModelSerializer):

    auctions = HyperlinkedIdentityField(
        view_name="member-auction-list",
        lookup_field="username",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "auctions",
        )
