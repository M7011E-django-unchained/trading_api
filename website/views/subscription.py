from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from website.models.subscription import Subscription
from website.serializer import SubscriptionListSerializer


class SubscriptionPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "list":
            return True
        elif view.action == "create":
            return request.user.is_authenticated


class SubscriptionList(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer
    permission_classes = [SubscriptionPermission]

    def get_queryset(self):
        return Subscription.objects.filter(userID=self.request.user)

    def perform_create(self, serializer):
        serializer.save(userID=self.request.user)
