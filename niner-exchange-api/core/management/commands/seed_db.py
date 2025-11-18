import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

# Import all your models
from core.models.user import CustomUser
from core.models.listing import (
    Listing,
    ItemListing,
    TextbookListing,
    Sublease,
    Service,
)

from core.models.image import Image


class Command(BaseCommand):
    help = "Seeds the database with initial data for users, listings, and images"

    def handle(self, *args, **options):
        # 0. Start with a clean slate
        self.stdout.write("Deleting old data...")
        # Delete in an order that respects foreign keys
        Image.objects.all().delete()
        Listing.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating new users...")

        # 1. Create users
        user1 = CustomUser.objects.create_user(
            email="pgarces@charlotte.edu",
            password="password123",
            first_name="Pablo",
            last_name="Garces",
            is_active=True,
            is_verified_student=True,
        )

        user2 = CustomUser.objects.create_user(
            email="skiser18@charlotte.edu",
            password="password123",
            first_name="Sean",
            last_name="Kiser",
            is_active=True,
            is_verified_student=True,
        )

        self.stdout.write(f"Created user: {user1.email}")
        self.stdout.write(f"Created user: {user2.email}")

        # 2. Create listings and link images
        self.stdout.write("Creating new listings and images...")

        # --- Listing 1: Textbook ---
        l1 = TextbookListing.objects.create(
            seller=user1,
            title="Intro to CS Textbook (ITSC 1212)",
            description="Used, but in great condition. No highlighting.",
            price=Decimal("45.00"),
            condition="LIKE_NEW",
            course_code="ITSC1212",
            price_new=Decimal("120.00"),
        )
        # Link an image to Listing 1
        Image.objects.create(
            listing=l1,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440511/lg4aJlc_z4xy0a.jpg",
        )

        # --- Listing 2: Item ---
        l2 = ItemListing.objects.create(
            seller=user2,
            title="Mini Fridge (Black)",
            description="Works perfectly, just don't need it anymore. Great for dorms.",
            price=Decimal("75.00"),
            condition="USED",
            price_new=Decimal("150.00"),
        )
        # Link an image to Listing 2
        Image.objects.create(
            listing=l2,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440495/eVQZeqz_ux3arn.jpg",  # Placeholder mini-fridge
        )

        # --- Listing 3: Sublease ---
        l3 = Sublease.objects.create(
            seller=user2,
            title="Room at U-Walk (Spring 2026)",
            description="Looking for a clean roommate. Private bathroom. Utilities included.",
            price=Decimal("850.00"),
            property_type="APARTMENT",
            start_date=timezone.datetime(2026, 1, 1),
            end_date=timezone.datetime(2026, 5, 15),
            number_of_bedrooms=4,
            number_of_roommates=3,
            distance_from_campus_minutes=10,
            physical_address="9505 University Terrace Dr",
        )
        # Link an image to Listing 3
        Image.objects.create(
            listing=l3,
            upload_order=1,
            image="https://www.americancampus.com/getmedia/02ee70ca-3b75-4e16-897c-54ebb743e6f0/474_13_Gallery_730x547.jpg",  # Placeholder apartment
        )

        # --- Listing 4: Service ---
        l4 = Service.objects.create(
            seller=user1,
            title="Math Tutoring (Calculus 1 & 2)",
            description="I can help you ace your final. $25/hr. Available evenings.",
            price=Decimal("25.00"),
            rate_type="HOURLY",
        )
        # Link an image to Listing 4
        Image.objects.create(
            listing=l4,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440441/math-tutor-charlotte_yeps4p.jpg",  # Placeholder tutoring/math
        )

        self.stdout.write(
            self.style.SUCCESS(
                "\nSuccessfully seeded the database with 2 users, 4 listings, and 4 images!"
            )
        )
