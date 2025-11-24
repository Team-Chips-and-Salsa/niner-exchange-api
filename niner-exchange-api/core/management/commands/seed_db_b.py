import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from core.models.user import CustomUser
from core.models.listing import (
    Listing,
    ItemListing,
    TextbookListing,
    Sublease,
    Service,
)
from core.models.image import Image
from core.models.meetup_location import MeetupLocation
from core.models.transaction import Transaction
from core.models.review import Review
from core.models.report import Report


class Command(BaseCommand):
    help = "Seeds the database with initial data (Version B)"

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        # Delete dependent objects first to avoid integrity errors if cascades aren't perfect
        Report.objects.all().delete()
        Review.objects.all().delete()
        Transaction.objects.all().delete()
        Image.objects.all().delete()
        Listing.objects.all().delete()
        MeetupLocation.objects.all().delete()
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
            email="user1@charlotte.edu",
            password="password123",
            first_name="User",
            last_name="One",
            profile_image_url="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000296/User1_qthue6.jpg",
            is_active=True,
            is_verified_student=True,
        )

        user2 = CustomUser.objects.create_user(
            email="user2@charlotte.edu",
            password="password123",
            first_name="User",
            last_name="Two",
            profile_image_url="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000296/user2_ptdc5b.jpg",
            is_active=True,
            is_verified_student=True,
        )

        self.stdout.write(f"Created user: {user1.email}")
        self.stdout.write(f"Created user: {user2.email}")

        # 2. CREATE MEETUP LOCATIONS
        self.stdout.write("Creating meetup locations...")
        loc1 = MeetupLocation.objects.create(
            name="Student Union",
            description="Main entrance of the Student Union.",
            latitude=35.3075,
            longitude=-80.734,
        )
        loc2 = MeetupLocation.objects.create(
            name="Atkins Library",
            description="Front desk area of the library.",
            latitude=35.306,
            longitude=-80.732,
        )
        self.stdout.write(f"Created locations: {loc1.name}, {loc2.name}")

        # 3. Create listings
        self.stdout.write("Creating listings...")

        # --- User 1 Listings (6 total) ---

        # 1. Textbook (Active)
        l1 = TextbookListing.objects.create(
            seller=user1,
            title="Baseball: Through History and Playing I",
            description="Good condition.",
            price=Decimal("30.00"),
            listing_type="TEXTBOOK",
            condition="USED",
            course_code="EXER2333",
            status="ACTIVE",
        )
        Image.objects.create(listing=l1, upload_order=1, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000298/textbook1_kelh3a.jpg")
        Image.objects.create(listing=l1, upload_order=2, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000297/textbook2_g4hrn2.jpg")
        Image.objects.create(listing=l1, upload_order=3, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000295/textbook3_s9cti0.jpg")

        # 2. Item (Active)
        l2 = ItemListing.objects.create(
            seller=user1,
            title="Wireless Mouse",
            description="Works great.",
            price=Decimal("15.00"),
            listing_type="ITEM",
            condition="LIKE_NEW",
            status="ACTIVE",
        )
        Image.objects.create(listing=l2, upload_order=1, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000294/mouse2_s8xdpc.jpg")
        Image.objects.create(listing=l2, upload_order=2, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000294/mouse1_sfis5p.jpg")

        # 3. Sublease (Active)
        l3 = Sublease.objects.create(
            seller=user1,
            title="Summer Sublease",
            description="Available June-August.",
            price=Decimal("600.00"),
            listing_type="SUBLEASE",
            property_type="APARTMENT",
            start_date=timezone.datetime(2026, 6, 1),
            end_date=timezone.datetime(2026, 8, 15),
            number_of_bedrooms=2,
            number_of_roommates=1,
            distance_from_campus_minutes=5,
            physical_address="100 University Blvd",
            status="ACTIVE",
        )
        Image.objects.create(listing=l3, upload_order=1, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000298/sublease2_skfyfg.jpg")
        Image.objects.create(listing=l3, upload_order=2, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000298/sublease_ndmekk.jpg")

        # 4. Service (Active)
        l4 = Service.objects.create(
            seller=user1,
            title="Math Tutoring",
            description="I can help you Ace your Math classes!",
            price=Decimal("15.00"),
            listing_type="SERVICE",
            rate_type="HOURLY",
            status="ACTIVE",
        )
        Image.objects.create(listing=l4, upload_order=1, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1763440441/math-tutor-charlotte_yeps4p.jpg")

        # 5. Item (Sold to User 2)
        l5_sold = ItemListing.objects.create(
            seller=user1,
            title="Gaming Keyboard",
            description="RGB mechanical keyboard.",
            price=Decimal("100.00"),
            listing_type="ITEM",
            condition="USED",
            status="SOLD",
        )
        Image.objects.create(listing=l5_sold, upload_order=1, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000294/keyboard1_i475se.jpg")
        Image.objects.create(listing=l5_sold, upload_order=2, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000294/keyboard2_jclpfu.jpg")

        # 6. Item (Sold to User 2)
        l6_sold = ItemListing.objects.create(
            seller=user1,
            title="Monitor 27 inch",
            description="1080p monitor.",
            price=Decimal("150.00"),
            listing_type="ITEM",
            condition="USED",
            status="SOLD",
        )
        Image.objects.create(listing=l6_sold, upload_order=1, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000294/monitor1_wkv8mw.jpg")
        Image.objects.create(listing=l6_sold, upload_order=2, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000294/monitor2_n2l3dy.jpg")

        # --- User 2 Listings (1 total) ---

        # 7. Item (Active) - Reported by User 1
        l7_reported = ItemListing.objects.create(
            seller=user2,
            title="Empress Eugénie Tiara",
            description="Too good to be true.",
            price=Decimal("5.00"),
            listing_type="ITEM",
            condition="NEW",
            status="ACTIVE",
        )
        Image.objects.create(listing=l7_reported, upload_order=1, image="https://res.cloudinary.com/dtdzbyryo/image/upload/v1764000973/toogood_fvejrs.jpg")

        self.stdout.write("Created listings.")

        # 4. Create Transactions
        self.stdout.write("Creating transactions...")

        # Transaction 1: User 2 bought l5_sold
        t1 = Transaction.objects.create(
            listing=l5_sold,
            buyer=user2,
            seller=user1,
            meetup_location=loc1,
            final_price=l5_sold.price,
            status="COMPLETED",
        )

        # Transaction 2: User 2 bought l6_sold
        t2 = Transaction.objects.create(
            listing=l6_sold,
            buyer=user2,
            seller=user1,
            meetup_location=loc2,
            final_price=l6_sold.price,
            status="COMPLETED",
        )
        self.stdout.write("Created transactions.")

        # 5. Create Reviews
        self.stdout.write("Creating reviews...")

        # Review 1: Normal review for T1
        Review.objects.create(
            transaction=t1,
            reviewer=user2,
            reviewee=user1,
            rating=5,
            comment="Great keyboard, thanks!",
            status="ACTIVE",
        )

        # Review 2: Inappropriate review for T2
        r2_inappropriate = Review.objects.create(
            transaction=t2,
            reviewer=user2,
            reviewee=user1,
            rating=1,
            comment="Terrible! I hate this! (Inappropriate content)",
            status="ACTIVE",
        )
        self.stdout.write("Created reviews.")

        # 6. Create Reports
        self.stdout.write("Creating reports...")

        # Report 1: User 1 reports User 2's listing (l7_reported)
        Report.objects.create(
            reporter=user1,
            content_type=ContentType.objects.get_for_model(Listing),
            object_id=l7_reported.listing_id,
            reason="SCAM",
            description="This looks like a scam listing.",
            status="PENDING",
        )

        # Report 2: User 1 reports User 2's profile
        Report.objects.create(
            reporter=user1,
            content_type=ContentType.objects.get_for_model(CustomUser),
            object_id=user2.id,
            reason="HARASSMENT",
            description="User is harassing me in messages.",
            status="PENDING",
        )

        # Report 3: User 1 reports User 2's inappropriate review (r2_inappropriate)
        Report.objects.create(
            reporter=user1,
            content_type=ContentType.objects.get_for_model(Review),
            object_id=r2_inappropriate.review_id,
            reason="INNAPROPRIATE",
            description="Review contains offensive language.",
            status="PENDING",
        )
        self.stdout.write("Created reports.")

        self.stdout.write(
            self.style.SUCCESS(
                "\nSuccessfully seeded the database (Version B)!"
            )
        )
