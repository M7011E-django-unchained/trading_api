from django.urls import path
from website.views import (
    AuctionList,
    AuctionDetail,
    MemberAuctionList,
    CategoryAuctionList,
    SubcategoryAuctionList,
    AuctionDeleteByUser,
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
        "User/<str:username>",
        MemberAuctionList.as_view({"get": "list"}),
        name="member-auction-list",
    ),
    path(
        "Category/<slug:name>",
        CategoryAuctionList.as_view(),
        name="category-auction-list",
    ),
    path(
        "Subcategory/<slug:subcategory_name>",
        SubcategoryAuctionList.as_view(),
        name="subcategory-auction-list",
    ),
    path(
        "delete/User/<str:username>",
        AuctionDeleteByUser.as_view(),
        name="auction-delete-by-user",
    ),
]
