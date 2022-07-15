from django.urls import path, include
from .views import Home, ReviewPage, LoginSuccess, MyTokenObtainPairView, ReviewList, StoreList, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'review'
urlpatterns = [
    path('', Home , name="Home"),
    path('success/', LoginSuccess, name="LoginSuccess"),
    path('review/<slug:store_slug>/', ReviewPage.as_view(), name="ReviewPage"),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/review/<int:store_id>/', ReviewList.as_view(), name='list_review'),
    path('api/store/', StoreList.as_view(), name='list_store'),
    path('api/register/', RegisterView.as_view()),
]