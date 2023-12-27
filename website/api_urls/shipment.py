from django.urls import path

from website.views import ShipmentList, ShipmentDetail

urlpatterns = [
    path(
        "", ShipmentList.as_view({"get": "list", "post": "create"}),
        name="shipment-list",
    ),
    path(
        "<int:pk>",
        ShipmentDetail.as_view(),
        name="shipment-detail",
    ),
]
