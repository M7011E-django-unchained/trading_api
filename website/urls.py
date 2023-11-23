from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    path("getAuction/", views.AuctionList.as_view(), name="auction_list"),
    path(
        "getAuction/<str:auctionID>/",
        views.AuctionDetail.as_view(),
        name="auction_detail",
    ),
    path("getCategory/", views.CategoryList.as_view(), name="category_list"),
    path(
        "getCategory/<str:name>",
        views.CategoryDetail.as_view(),
        name="category_detail",
    ),
]
