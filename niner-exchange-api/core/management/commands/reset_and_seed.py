import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = "Wipes the database, runs migrations, and seeds data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--seed-b",
            action="store_true",
            help="Use seed_db_b instead of the default seed_db",
        )
        parser.add_argument(
            "--seed-c",
            action="store_true",
            help="Use seed_db_c (4 Zones, 1 Admin)",
        )
        parser.add_argument(
            "--no-seed",
            action="store_true",
            help="Skip seeding step (leaves database empty)",
        )
        parser.add_argument(
            "--hard",
            action="store_true",
            help="Hard reset: Drops all tables/schema before migrating. WARNING: Destructive!",
        )

    def handle(self, *args, **options):
        if options["hard"]:
            self.stdout.write(self.style.WARNING("Performing HARD reset..."))
            
            vendor = connection.vendor
            if vendor == "sqlite":
                db_name = settings.DATABASES["default"]["NAME"]
                if os.path.exists(db_name):
                    self.stdout.write(f"Deleting SQLite file: {db_name}")
                    # Close connection before deleting
                    connection.close()
                    os.remove(db_name)
                else:
                    self.stdout.write("SQLite file not found, skipping delete.")
            
            elif vendor == "postgresql":
                self.stdout.write("Dropping public schema...")
                with connection.cursor() as cursor:
                    cursor.execute("DROP SCHEMA public CASCADE;")
                    cursor.execute("CREATE SCHEMA public;")
            
            else:
                self.stdout.write(self.style.ERROR(f"Hard reset not implemented for vendor: {vendor}"))
                return

        else:
            self.stdout.write(self.style.WARNING("Flushing database..."))
            call_command("flush", "--no-input")

        self.stdout.write(self.style.SUCCESS("Making migrations..."))
        call_command("makemigrations")

        self.stdout.write(self.style.SUCCESS("Migrating..."))
        call_command("migrate")

        if options["no_seed"]:
            self.stdout.write(self.style.SUCCESS("Skipping seeding (Database is empty)."))
        elif options["seed_b"]:
            self.stdout.write(self.style.SUCCESS("Seeding database (Version B)..."))
            call_command("seed_db_b")
        elif options["seed_c"]:
            self.stdout.write(self.style.SUCCESS("Seeding database (Version C)..."))
            call_command("seed_db_c")
        else:
            self.stdout.write(self.style.SUCCESS("Seeding database (Default)..."))
            call_command("seed_db")

        self.stdout.write(self.style.SUCCESS("\nDatabase reset and seeded successfully!"))
