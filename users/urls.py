from django.urls import path

from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('update/', views.UpdateUser.as_view(), name='update'),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
