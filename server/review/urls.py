from django.urls import path, include
from .views import Home, ReviewPage, LoginSuccess, MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'review'
urlpatterns = [
    path('', Home , name="Home"),
    path('success/', LoginSuccess, name="LoginSuccess"),
    path('review/<str:store_name>/', ReviewPage.as_view(), name="ReviewPage"),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]