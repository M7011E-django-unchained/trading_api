from django.urls import path
from . import views

urlpatterns = [
    path("getAuction/", views.AuctionList.as_view(), name="auction_list"),
    path(
        "getAuction/<int:auctionID>/",
        views.AuctionDetail.as_view(),
        name="auction_detail",
    ),
    path("getCategory/", views.CategoryList.as_view(), name="category_list"),
    path(
        "getCategory/<str:name>",
        views.CategoryDetail.as_view(),
        name="category_detail",
    ),
    path("getMember/", views.MemberList.as_view(), name="member_list"),
    path(
        "getMember/<str:username>/", views.MemberDetail.as_view(), name="member_detail"
    ),
]
