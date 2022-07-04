from django.db import models

# Create your models here.

class Review(models.Model):
    customer_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11)
    technician_assigned = models.CharField(max_length=20)
