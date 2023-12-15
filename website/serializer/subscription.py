from django.contrib.auth.models import User
from rest_framework.relations import HyperlinkedIdentityField, \
    HyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer

from website.models import Subscription
from website.serializer import MemberDetailSerializer, UserDetailSerializer


class SubscriptionListSerializer(HyperlinkedModelSerializer):
    user_name = HyperlinkedRelatedField(
        view_name="member-detail",
        lookup_field="username",
        queryset=User.objects.all(),
    )

    HyperlinkedIdentityField(
        view_name="auction-detail",
        lookup_field="auctionID",
    )

    class Meta:
        model = Subscription
        fields = ['userID', 'auctionID']
