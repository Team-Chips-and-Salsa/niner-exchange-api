import uuid

from django.conf import settings
from django.db import models

from core.models.category import Category


class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CONDITIONS = [
        ('USED', 'Used'),
        ('LIKE_NEW', 'Like New'),
        ('NEW', 'New'),
    ]
    condition = models.CharField(max_length=11, choices=CONDITIONS, default='USED')
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold'),
        ('REMOVE', 'Remove'),
    ]
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title