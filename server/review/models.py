from random import choices
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.

STATUS_MESSAGE = (
    (0, 'Success'),
    (1, 'Failed')
)

class Customer(models.Model):
    full_name = models.CharField(max_length=55, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    email = models.CharField(max_length=55, null=True, blank=True)

class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_users')
    store_name = models.CharField(max_length=20, unique=True)
    store_slug = models.SlugField(max_length=50, null=True, blank=True, unique=True)
    logo = models.CharField(max_length=255)
    title = models.CharField(max_length=50)
    message = models.TextField()
    message2 = models.TextField(null=True, blank=True)
    domain = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    url_map_store = models.TextField()
    customer = models.ManyToManyField(Customer, related_name='store_customers', blank=True)

    def save(self, *args, **kwargs):
        self.store_slug = slugify(self.store_name)
        super(Store, self).save(*args, **kwargs)

class Review(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    review_score = models.IntegerField()
    review_content = models.TextField(null=True, blank=True)
    review_email = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MessageLog(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    from_phone = models.CharField(max_length=12)
    to_phone = models.CharField(max_length=12)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS_MESSAGE, default=0)
    sid = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

