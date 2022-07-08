from django.urls import path, include
from .views import Home, ReviewPage

app_name = 'review'
urlpatterns = [
    path('abc', Home , name="Home"),
    path('review/<str:store_name>/', ReviewPage.as_view(), name="ReviewPage"),
]