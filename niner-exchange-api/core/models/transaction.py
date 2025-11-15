from django.db import models
from django.conf import settings

import uuid

from core.models.listing import Listing
from core.models.meetup_location import MeetupLocation


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="purchases", on_delete=models.CASCADE
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sales", on_delete=models.CASCADE
    )
    meetup_location = models.ForeignKey(
        MeetupLocation, on_delete=models.SET_NULL, null=True, blank=True
    )
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.status}"
