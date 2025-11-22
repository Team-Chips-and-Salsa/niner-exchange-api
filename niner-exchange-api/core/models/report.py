from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import UniqueConstraint

# Used Gemini guided learning to help me figure out how to represent the three different types of reports by using a GFK
class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Content type I learned will help distinguish between different types of reports by assigning an ID to each model (user, review, listing)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # This refers to the listing's listing_id for example
    object_id = models.UUIDField(primary_key=False)
    # This holds the actual model of a listing for example. It is found by using content_type and object_id
    content_object = GenericForeignKey('content_type', 'object_id')

    REASON_CHOICES = [
        ("SPAM", "Spam"),
        ("INNAPROPRIATE", "Innapropriate"),
        ("HARASSMENT", "Harassment"),
        ("SCAM", "Scam"),
        ("OTHER", "Other"),
    ]

    reason = models.CharField(max_length=13, choices=REASON_CHOICES)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default="PENDING")
    description = models.TextField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['object_id', 'reporter'], name='only-one-report')
        ]