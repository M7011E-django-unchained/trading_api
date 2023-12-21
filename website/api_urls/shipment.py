from django.urls import path

from website.views import ShipmentList

urlpatterns = [
    path(
        "", ShipmentList.as_view({"get": "list", "post": "create"}),
        name="shipment-list",
    ),

]
