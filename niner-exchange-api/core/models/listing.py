import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


# Used AI to figure out that Multi-Table Inheritance is a better approach here
class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("1"))],
    )

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("SOLD", "Sold"),
        ("REMOVE", "Remove"),
    ]
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=1), name="listing_price_min_1"
            ),
        ]

    def __str__(self):
        return self.title


class PhysicalListing(Listing):
    CONDITIONS = [
        ("USED", "Used"),
        ("LIKE_NEW", "Like New"),
        ("NEW", "New"),
    ]
    condition = models.CharField(max_length=11, choices=CONDITIONS)
    price_new = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )


class ItemListing(PhysicalListing):
    pass


class TextbookListing(PhysicalListing):
    course_code = models.CharField(max_length=20)


class Sublease(Listing):
    PROPERTY_TYPE = [("APARTMENT", "Apartment"), ("HOUSE", "House")]
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_bedrooms = models.IntegerField(validators=[MinValueValidator(1)])
    number_of_roommates = models.IntegerField(validators=[MinValueValidator(1)])
    distance_from_campus_minutes = models.IntegerField(
        validators=[MinValueValidator(1)]
    )


class Service(Listing):
    pass
