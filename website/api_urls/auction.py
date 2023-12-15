from django.urls import path
from website.views import (
    AuctionList,
    AuctionDetail,
    MemberAuctionList,
    CategoryAuctionList,
    SubcategoryAuctionList,
)

urlpatterns = [
    path(
        "",
        AuctionList.as_view({"get": "list", "post": "create"}),
        name="auction-list",
    ),
    path(
        "<int:auctionID>",
        AuctionDetail.as_view(),
        name="auction-detail",
    ),
    path(
        "user/<str:username>",
        MemberAuctionList.as_view({"get": "list"}),
        name="member-auction-list",
    ),
    path(
        "category/<slug:name>",
        CategoryAuctionList.as_view(),
        name="category-auction-list",
    ),
    path(
        "subcategory/<slug:subcategory_name>",
        SubcategoryAuctionList.as_view(),
        name="subcategory-auction-list",
    ),
    path("subscribe/<int:auctionID>", AuctionDetail.as_view(),
         name="subscribe"),

]
