from django.db import models

# Create your models here.

class Review(models.Model):
    customer_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11)
    review_score = models.IntegerField()
    review_content = models.CharField(max_length=255)
    review_email = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


