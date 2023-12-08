from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('update/', views.UpdateUser.as_view(), name='update'),
]
