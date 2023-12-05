from django.urls import path
from . import views

urlpatterns = [
    path("getAuction/", views.AuctionList.as_view(), name="auction-list"),
    path(
        "getAuction/<int:auctionID>/",
        views.AuctionDetail.as_view(),
        name="auction-detail",
    ),
    path(
        "getAuctionsByUser/<str:username>",
        views.MemberAuctionList.as_view(),
        name="member-auction-list",
    ),
    path(
        "getAuctionsByCategory/<slug:name>",
        views.CategoryAuctionList.as_view(),
        name="category-auction-list",
    ),
    path(
        "getCategory/",
        views.CategoryList.as_view({"get": "list", "post": "create"}),
        name="category-list",
    ),
    path(
        "getCategory/<slug:name>",
        views.CategoryDetail.as_view(),
        name="category-detail",
    ),
    path(
        "getSubcategory/",
        views.SubcategoryList.as_view({"get": "list", "post": "create"}),
        name="subcategory-list",
    ),
    path(
        "getSubategory/<slug:subcategory_name>",
        views.SubcategoryDetail.as_view(),
        name="subcategory-detail",
    ),
    path(
        "getMember/",
        views.MemberList.as_view(),
        name="member-list",
    ),
    path(
        "getMember/<str:username>/", views.MemberDetail.as_view(),
        name="member-detail"
    ),
]
