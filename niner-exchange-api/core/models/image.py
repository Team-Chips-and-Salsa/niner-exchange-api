import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models.listing import Listing


class Image(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    imageUrl = models.TextField(null=False)
    # Limit range to 1-3
    uploadOrder = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(1)])