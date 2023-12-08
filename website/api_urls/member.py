from django.urls import path

from website.views import MemberList, MemberDetail

urlpatterns = [
    path(
        "",
        MemberList.as_view(),
        name="member-list",
    ),
    path("<str:username>/", MemberDetail.as_view(), name="member-detail"),
]
