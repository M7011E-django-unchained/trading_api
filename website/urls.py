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
        "getCategory/",
        views.CategoryList.as_view({"get": "list", "post": "create"}),
        name="category-list",
    ),
    path(
        "getCategory/<str:name>",
        views.CategoryDetail.as_view(),
        name="category-detail",
    ),
    path(
        "getSubcategory/",
        views.SubcategoryList.as_view(),
        name="subcategory-list",
    ),
    path(
        "getSubcategory/<str:name>",
        views.SubcategoryDetail.as_view(),
        name="subcategory-detail",
    ),
    path("getMember/", views.MemberList.as_view(), name="member-list"),
    path(
        "getMember/<str:username>/", views.MemberDetail.as_view(), name="member-detail"
    ),
]
