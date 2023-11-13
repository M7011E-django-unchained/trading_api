from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    path("auction-list/", views.auctionList, name="auction-list"),
    path("auction-detail/<str:id>/", views.auctionDetail, name="auction-detail"),
    path("auction-create/", views.auctionCreate, name="auction-create"),
    path("auction-update/<str:id>/", views.auctionUpdate, name="auction-update"),
    path("auction-delete/<str:id>/", views.auctionDelete, name="auction-delete"),
    path("user-list/", views.userList, name="user-list"),
    path("user-detail/<str:id>/", views.userDetail, name="user-detail"),
    path("user-create/", views.userCreate, name="user-create"),
]
