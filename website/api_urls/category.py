from django.urls import path

from website.views import CategoryList, CategoryDetail

urlpatterns = [
    path(
        "",
        CategoryList.as_view({"get": "list", "post": "create"}),
        name="category-list",
    ),
    path(
        "<slug:name>",
        CategoryDetail.as_view(),
        name="category-detail",
    ),
]
