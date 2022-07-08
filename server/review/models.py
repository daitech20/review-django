from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_users')
    store_name = models.CharField(max_length=20, unique=True)
    logo = models.CharField(max_length=255)
    title = models.CharField(max_length=50)
    message = models.TextField()
    domain = models.CharField(max_length=50)
    customer = models.ManyToManyField(User, related_name='store_customers', blank=True)

class Review(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    review_score = models.IntegerField()
    review_content = models.TextField(null=True, blank=True)
    review_email = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



