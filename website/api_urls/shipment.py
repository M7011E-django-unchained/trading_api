from django.urls import path

from website.views import (
    ShipmentList, ShipmentDetail, ShipmentPaid, ShipmentUnpaid,
    ShipmentShipped, ShipmentUnshipped, ShipmentUserList, ShipmentByAuction)

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
    path("paid/", ShipmentPaid.as_view(), name="shipment-paid"),
    path("unpaid/", ShipmentUnpaid.as_view(), name="shipment-unpaid"),
    path("shipped/", ShipmentShipped.as_view(), name="shipment-shipped"),
    path("unshipped/", ShipmentUnshipped.as_view(), name="shipment-unshipped"),
    path("user/<int:pk>",
         ShipmentUserList.as_view(), name="shipment-user"),
    path("auction/<int:pk>", ShipmentByAuction.as_view(),
         name="shipment-auction")

]
