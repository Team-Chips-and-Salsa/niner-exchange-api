from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Wipes the database, runs migrations, and seeds data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--seed-b",
            action="store_true",
            help="Use seed_db_b instead of the default seed_db",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Flushing database..."))
        call_command("flush", "--no-input")

        self.stdout.write(self.style.SUCCESS("Making migrations..."))
        call_command("makemigrations")

        self.stdout.write(self.style.SUCCESS("Migrating..."))
        call_command("migrate")

        if options["seed_b"]:
            self.stdout.write(self.style.SUCCESS("Seeding database (Version B)..."))
            call_command("seed_db_b")
        else:
            self.stdout.write(self.style.SUCCESS("Seeding database (Default)..."))
            call_command("seed_db")

        self.stdout.write(self.style.SUCCESS("\nDatabase reset and seeded successfully!"))
