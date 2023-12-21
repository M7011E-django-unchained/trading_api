from django.urls import path, include

urlpatterns = [
    path("auction/", include("website.api_urls.auction")),
    path("bid/", include("website.api_urls.bid")),
    path("subcategory/", include("website.api_urls.subcategory")),
    path("category/", include("website.api_urls.category")),
    path("member/", include("website.api_urls.member")),
    path("shipment/", include("website.api_urls.shipment")),
]
