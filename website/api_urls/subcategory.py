from django.urls import path

from website.views import SubcategoryList, SubcategoryDetail

urlpatterns = [
    path(
        "",
        SubcategoryList.as_view({"get": "list", "post": "create"}),
        name="subcategory-list",
    ),
    path(
        "<slug:subcategory_name>",
        SubcategoryDetail.as_view(),
        name="subcategory-detail",
    ),
]
