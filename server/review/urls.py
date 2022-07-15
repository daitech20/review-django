from django.urls import path, include
from .views import Home, ReviewPage, LoginSuccess, MyTokenObtainPairView,\
    ReviewList, StoreList, RegisterView, StoreDetail, StoreUpdate
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
    path('api/review/<slug:store_slug>/', ReviewList.as_view(), name='list_review'),
    path('api/store/', StoreList.as_view(), name='list_store'),
    path('api/store/detail/<slug:store_slug>/', StoreDetail.as_view(), name='detail_store'),
    path('api/store/update/<slug:store_slug>/', StoreUpdate.as_view(), name='update_store'),
    path('api/register/', RegisterView.as_view()),
]