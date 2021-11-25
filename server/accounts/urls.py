from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views


urlpatterns = [
    path('signup/', views.signup),
    path('profile/', views.profile),
    path('reviewed/<int:user_pk>/', views.reviewed_movie),
    path('api-token-auth/', obtain_jwt_token),
]
