from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
)
from django.contrib.auth.models import User
from website.models import Member


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']
        # TODO set min length later
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class profilePicSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ("profilePicPath",)


class UserDetailSerializer(ModelSerializer):
    profilePicPath = profilePicSerializer(
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
            'password',
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "profilePicPath",
            "auctions",
        )
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)
        profilePicPath = validated_data.pop('profilePicPath', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if email:
            user.email = email

        if profilePicPath:
            user.profilePicPath = profilePicPath

        user.save()
        return user
