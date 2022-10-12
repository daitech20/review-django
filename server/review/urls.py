from django.urls import path, include
from .views import Home, ReviewPage, LoginSuccess, MyTokenObtainPairView,\
    ReviewList, StoreList, RegisterView, StoreDetail, StoreUpdate, UserDetail,\
    ChangePassword, CustomerList, CustomerUpdate, StoreCreate, UserList,\
    ResetPassword, SocialApplicationUpdate, StoreAddCustomer, SendAllMessage, SendMessage, \
    MessageLogList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'review'
urlpatterns = [
    path('', Home , name="Home"),
    path('success/', LoginSuccess, name="LoginSuccess"),
    path('review/<slug:store_slug>/', ReviewPage.as_view(), name="ReviewPage"),
	path('api/user/', UserList.as_view(), name="list_user"),
    path('api/user/<str:username>/', UserDetail.as_view()),
    path('api/user/change/password/<str:username>/', ChangePassword.as_view(), name = "change_password"),
    path('api/user/reset/password/<str:username>/', ResetPassword.as_view(), name = "reset_password"),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/review/<slug:store_slug>/', ReviewList.as_view(), name='list_review'),
    path('api/store/', StoreList.as_view(), name='list_store'),
    path('api/store/create/', StoreCreate.as_view(), name='create_store'),
    path('api/store/detail/<slug:store_slug>/', StoreDetail.as_view(), name='detail_store'),
    path('api/store/update/<slug:store_slug>', StoreUpdate.as_view(), name='update_store'),
    path('api/store/addCustomer/<slug:store_slug>', StoreAddCustomer.as_view(), name='add_customer'),
    path('api/customer/<slug:store_slug>/', CustomerList.as_view(), name='list_customer'),
    path('api/customer/update/<int:id>/', CustomerUpdate.as_view(), name='update_customer'),
    path('api/register/', RegisterView.as_view()),
    path('api/social/application/<int:pk>/', SocialApplicationUpdate.as_view(), name='update_social_application'),
    path('api/sendMessage/<slug:store_slug>/', SendAllMessage.as_view(), name='send_all_message'),
    path('api/sendMessage/<slug:store_slug>/<str:customer_id>/', SendMessage.as_view(), name='send_message'),
    path('api/messageLog/<slug:store_slug>/', MessageLogList.as_view(), name='message_log_list'),

]