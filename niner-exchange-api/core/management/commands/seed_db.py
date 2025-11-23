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
            email="test1@charlotte.com",
            password="password123",
            first_name="Test",
            last_name="1",
            is_active=True,
            is_verified_student=True,
        )

        user2 = CustomUser.objects.create_user(
            email="test2@charlotte.com",
            password="password123",
            first_name="Test",
            last_name="2",
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

        # --- Listing 5: Textbook ---
        l5 = TextbookListing.objects.create(
            seller=user2,
            title="Data Structures Textbook (ITSC 2214)",
            description="Excellent condition, minimal wear. Includes practice problems.",
            price=Decimal("55.00"),
            listing_type="TEXTBOOK",
            condition="LIKE_NEW",
            course_code="ITSC2214",
            price_new=Decimal("135.00"),
        )
        Image.objects.create(
            listing=l5,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440511/lg4aJlc_z4xy0a.jpg",
        )

        # --- Listing 6: Textbook ---
        l6 = TextbookListing.objects.create(
            seller=user1,
            title="Calculus I Textbook (MATH 1241)",
            description="Some highlighting, good condition overall.",
            price=Decimal("40.00"),
            listing_type="TEXTBOOK",
            condition="USED",
            course_code="MATH1241",
            price_new=Decimal("110.00"),
        )
        Image.objects.create(
            listing=l6,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440511/lg4aJlc_z4xy0a.jpg",
        )

        # --- Listing 7: Textbook ---
        l7 = TextbookListing.objects.create(
            seller=user2,
            title="Chemistry Lab Manual (CHEM 1251)",
            description="Brand new, never used. Still in shrink wrap.",
            price=Decimal("30.00"),
            listing_type="TEXTBOOK",
            condition="NEW",
            course_code="CHEM1251",
            price_new=Decimal("65.00"),
        )
        Image.objects.create(
            listing=l7,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440511/lg4aJlc_z4xy0a.jpg",
        )

        # --- Listing 8: Textbook ---
        l8 = TextbookListing.objects.create(
            seller=user1,
            title="Physics for Engineers (PHYS 2101)",
            description="Good condition, some notes in margins.",
            price=Decimal("50.00"),
            listing_type="TEXTBOOK",
            condition="USED",
            course_code="PHYS2101",
            price_new=Decimal("140.00"),
        )
        Image.objects.create(
            listing=l8,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440511/lg4aJlc_z4xy0a.jpg",
        )

        # --- Listing 9: Item ---
        l9 = ItemListing.objects.create(
            seller=user1,
            title="Desk Lamp (LED)",
            description="Adjustable brightness, perfect for studying. Like new.",
            price=Decimal("20.00"),
            listing_type="ITEM",
            condition="LIKE_NEW",
            price_new=Decimal("45.00"),
        )
        Image.objects.create(
            listing=l9,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440495/eVQZeqz_ux3arn.jpg",
        )

        # --- Listing 10: Item ---
        l10 = ItemListing.objects.create(
            seller=user2,
            title="Microwave Oven",
            description="Works great, clean. Moving out sale.",
            price=Decimal("40.00"),
            listing_type="ITEM",
            condition="USED",
            price_new=Decimal("80.00"),
        )
        Image.objects.create(
            listing=l10,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440495/eVQZeqz_ux3arn.jpg",
        )

        # --- Listing 11: Item ---
        l11 = ItemListing.objects.create(
            seller=user1,
            title="Office Chair (Ergonomic)",
            description="Comfortable chair, adjustable height. Minor wear.",
            price=Decimal("60.00"),
            listing_type="ITEM",
            condition="USED",
            price_new=Decimal("150.00"),
        )
        Image.objects.create(
            listing=l11,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440495/eVQZeqz_ux3arn.jpg",
        )

        # --- Listing 12: Item ---
        l12 = ItemListing.objects.create(
            seller=user2,
            title="Coffee Maker (Keurig)",
            description="Single serve, works perfectly. Includes some pods.",
            price=Decimal("35.00"),
            listing_type="ITEM",
            condition="LIKE_NEW",
            price_new=Decimal("90.00"),
        )
        Image.objects.create(
            listing=l12,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440495/eVQZeqz_ux3arn.jpg",
        )

        # --- Listing 13: Sublease ---
        l13 = Sublease.objects.create(
            seller=user1,
            title="Room at The Edge (Summer 2026)",
            description="Fully furnished, pool access. Great location near campus.",
            price=Decimal("750.00"),
            listing_type="SUBLEASE",
            property_type="APARTMENT",
            start_date=timezone.datetime(2026, 5, 15),
            end_date=timezone.datetime(2026, 8, 15),
            number_of_bedrooms=2,
            number_of_roommates=1,
            distance_from_campus_minutes=5,
            physical_address="9100 University City Blvd",
        )
        Image.objects.create(
            listing=l13,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763474116/474_13_Gallery_730x547_ysnbox.jpg",
        )

        # --- Listing 14: Sublease ---
        l14 = Sublease.objects.create(
            seller=user2,
            title="Studio at Light Rail Apartments (Fall 2026)",
            description="Private studio, utilities included. Walking distance to campus.",
            price=Decimal("900.00"),
            listing_type="SUBLEASE",
            property_type="APARTMENT",
            start_date=timezone.datetime(2026, 8, 15),
            end_date=timezone.datetime(2026, 12, 15),
            number_of_bedrooms=1,
            number_of_roommates=0,
            distance_from_campus_minutes=15,
            physical_address="8825 JM Keynes Dr",
        )
        Image.objects.create(
            listing=l14,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763474116/474_13_Gallery_730x547_ysnbox.jpg",
        )

        # --- Listing 15: Sublease ---
        l15 = Sublease.objects.create(
            seller=user1,
            title="Room at Campus Edge (Spring 2026)",
            description="Shared bathroom, quiet roommates. Pet-friendly building.",
            price=Decimal("650.00"),
            listing_type="SUBLEASE",
            property_type="APARTMENT",
            start_date=timezone.datetime(2026, 1, 1),
            end_date=timezone.datetime(2026, 5, 15),
            number_of_bedrooms=3,
            number_of_roommates=2,
            distance_from_campus_minutes=8,
            physical_address="9610 University City Blvd",
        )
        Image.objects.create(
            listing=l15,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763474116/474_13_Gallery_730x547_ysnbox.jpg",
        )

        # --- Listing 16: Sublease ---
        l16 = Sublease.objects.create(
            seller=user2,
            title="House Room (Year Lease Available)",
            description="Large room in 4BR house. Backyard, parking included.",
            price=Decimal("700.00"),
            listing_type="SUBLEASE",
            property_type="HOUSE",
            start_date=timezone.datetime(2026, 1, 1),
            end_date=timezone.datetime(2027, 1, 1),
            number_of_bedrooms=4,
            number_of_roommates=3,
            distance_from_campus_minutes=12,
            physical_address="1234 University Area Dr",
        )
        Image.objects.create(
            listing=l16,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763474116/474_13_Gallery_730x547_ysnbox.jpg",
        )

        # --- Listing 17: Service ---
        l17 = Service.objects.create(
            seller=user1,
            title="Resume Review & Career Coaching",
            description="Help with resume, cover letters, and interview prep. Per session.",
            price=Decimal("30.00"),
            listing_type="SERVICE",
            rate_type="PER_SESSION",
        )
        Image.objects.create(
            listing=l17,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440441/math-tutor-charlotte_yeps4p.jpg",
        )

        # --- Listing 18: Service ---
        l18 = Service.objects.create(
            seller=user2,
            title="Photography Services (Events & Portraits)",
            description="Professional photos for events, headshots, or portraits. Hourly rate.",
            price=Decimal("50.00"),
            listing_type="SERVICE",
            rate_type="HOURLY",
        )
        Image.objects.create(
            listing=l18,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440441/math-tutor-charlotte_yeps4p.jpg",
        )

        # --- Listing 19: Service ---
        l19 = Service.objects.create(
            seller=user1,
            title="Web Development (Small Projects)",
            description="Build simple websites or fix bugs. Flat rate per project.",
            price=Decimal("100.00"),
            listing_type="SERVICE",
            rate_type="FLAT_RATE",
        )
        Image.objects.create(
            listing=l19,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440441/math-tutor-charlotte_yeps4p.jpg",
        )

        # --- Listing 20: Service ---
        l20 = Service.objects.create(
            seller=user2,
            title="Guitar Lessons (Beginner to Intermediate)",
            description="Learn acoustic or electric guitar. Flexible schedule. Hourly rate.",
            price=Decimal("35.00"),
            listing_type="SERVICE",
            rate_type="HOURLY",
        )
        Image.objects.create(
            listing=l20,
            upload_order=1,
            image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440441/math-tutor-charlotte_yeps4p.jpg",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "\nSuccessfully seeded the database with 3 users, 1 location, 20 listings, and 20 images!"
            )
        )
