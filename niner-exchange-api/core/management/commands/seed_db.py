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

# --- 1. IMPORT YOUR MEETUPLOCATION MODEL ---
from core.models.meetup_location import MeetupLocation


class Command(BaseCommand):
    help = "Seeds the database with initial data for users, listings, and images"

    def handle(self, *args, **options):
        # 0. Start with a clean slate
        self.stdout.write("Deleting old data...")
        # Delete in an order that respects foreign keys
        Image.objects.all().delete()
        Listing.objects.all().delete()
        MeetupLocation.objects.all().delete()  # --- ADDED ---
        CustomUser.objects.all().delete()

        self.stdout.write("Creating new users...")

        # 1. Create users
        admin = CustomUser.objects.create_superuser(
            email="admin@charlotte.edu",
            password="password123",
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_verified_student=True,
            is_superuser=True,
            role="admin",
        )
        self.stdout.write(f"Created user: {admin.email}")

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

        # --- 2. CREATE MEETUP LOCATION ---
        self.stdout.write("Creating meetup locations...")
        loc1 = MeetupLocation.objects.create(
            name="UNC Charlotte General Area",
            description="General location for the UNC Charlotte campus.",
            latitude=35.3075,
            longitude=-80.734,
        )
        self.stdout.write(f"Created location: {loc1.name}")

        # 3. Create listings and link images
        self.stdout.write("Creating new listings and images...")

        # --- Listing 1: Textbook ---
        l1 = TextbookListing.objects.create(
            seller=user1,
            title="Intro to CS Textbook (ITSC 1212)",
            description="Used, but in great condition. No highlighting.",
            price=Decimal("45.00"),
            listing_type="TEXTBOOK",
            condition="LIKE_NEW",
            course_code="ITSC1212",
            price_new=Decimal("120.00"),
        )
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
            listing_type="ITEM",  # --- ADDED ---
            condition="USED",
            price_new=Decimal("150.00"),
        )
        Image.objects.create(
            listing=l2,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440495/eVQZeqz_ux3arn.jpg",
        )

        # --- Listing 3: Sublease ---
        l3 = Sublease.objects.create(
            seller=user2,
            title="Room at U-Walk (Spring 2026)",
            description="Looking for a clean roommate. Private bathroom. Utilities included.",
            price=Decimal("850.00"),
            listing_type="SUBLEASE",
            property_type="APARTMENT",
            start_date=timezone.datetime(2026, 1, 1),
            end_date=timezone.datetime(2026, 5, 15),
            number_of_bedrooms=4,
            number_of_roommates=3,
            distance_from_campus_minutes=10,
            physical_address="9505 University Terrace Dr",
        )
        Image.objects.create(
            listing=l3,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763474116/474_13_Gallery_730x547_ysnbox.jpg",
        )

        # --- Listing 4: Service ---
        l4 = Service.objects.create(
            seller=user1,
            title="Math Tutoring (Calculus 1 & 2)",
            description="I can help you ace your final. $25/hr. Available evenings.",
            price=Decimal("25.00"),
            listing_type="SERVICE",  # --- ADDED ---
            rate_type="HOURLY",
        )
        Image.objects.create(
            listing=l4,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440441/math-tutor-charlotte_yeps4p.jpg",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "\nSuccessfully seeded the database with 3 users, 1 location, 4 listings, and 4 images!"
            )
        )
