from django.urls import path, include

urlpatterns = [
    path("auction/", include("website.api_urls.auction")),
    path("subcategory/", include("website.api_urls.subcategory")),
    path("category/", include("website.api_urls.category")),
    path("member/", include("website.api_urls.member")),
]
