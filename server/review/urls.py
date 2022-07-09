from django.urls import path, include
from .views import Home, ReviewPage, LoginSuccess

app_name = 'review'
urlpatterns = [
    path('', Home , name="Home"),
    path('success/', LoginSuccess, name="LoginSuccess"),
    path('review/<str:store_name>/', ReviewPage.as_view(), name="ReviewPage"),
]