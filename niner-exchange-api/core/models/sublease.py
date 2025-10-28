import uuid

from django.db import models

from core.models.listing import Listing
from django.core.validators import MinValueValidator


class Sublease(models.Model):
    sublease_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    PROPERTY_TYPE = [("APARTMENT", "Apartment"), ("HOUSE", "House")]
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_bedrooms = models.IntegerField(validators=[MinValueValidator(1)])
    number_of_roommates = models.IntegerField(validators=[MinValueValidator(1)])
    distance_from_campus_minutes = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"Sublease for {self.listing.title} from {self.start_date} to {self.end_date}"
