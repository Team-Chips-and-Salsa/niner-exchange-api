import uuid

from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models.listing import Listing


class Image(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    # Limit range to 1-3
    upload_order = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['listing', 'upload_order'],
                name='unique_listing_order'
            )
        ]

    def __str__(self):
        return f"Image {self.upload_order} for {self.listing.title}"
