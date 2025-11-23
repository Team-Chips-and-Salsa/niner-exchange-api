from django.core.management.base import BaseCommand
from core.models.user import CustomUser
from core.models.meetup_location import MeetupLocation
from core.models.listing import Listing
from core.models.image import Image
from core.models.transaction import Transaction
from core.models.review import Review
from core.models.report import Report


class Command(BaseCommand):
    help = "Seeds the database with initial data (Version C: 4 Zones, 1 Admin)"

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        # Delete dependent objects first
        Report.objects.all().delete()
        Review.objects.all().delete()
        Transaction.objects.all().delete()
        Image.objects.all().delete()
        Listing.objects.all().delete()
        MeetupLocation.objects.all().delete()
        CustomUser.objects.all().delete()

        self.stdout.write("Creating new users...")

        # 1. Create Admin
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

        # 2. CREATE MEETUP LOCATIONS
        self.stdout.write("Creating meetup locations...")
        
        loc1 = MeetupLocation.objects.create(
            name="Student Union",
            description="Main entrance of the Student Union.",
            latitude=35.3086,
            longitude=-80.7337,
        )
        
        loc2 = MeetupLocation.objects.create(
            name="Atkins Library",
            description="Front desk area of the library.",
            latitude=35.3057,
            longitude=-80.7323,
        )

        loc3 = MeetupLocation.objects.create(
            name="UREC",
            description="University Recreation Center entrance.",
            latitude=35.3095,
            longitude=-80.7350,
        )

        loc4 = MeetupLocation.objects.create(
            name="Dubois Center",
            description="Center City Building lobby.",
            latitude=35.2270,
            longitude=-80.8400,
        )

        self.stdout.write(f"Created locations: {loc1.name}, {loc2.name}, {loc3.name}, {loc4.name}")

        self.stdout.write(
            self.style.SUCCESS(
                "\nSuccessfully seeded the database (Version C)!"
            )
        )
