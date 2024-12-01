from django.core.management.base import BaseCommand
from django.utils.text import Truncator

from clubs.models import Venue, Table

class Command(BaseCommand):
    help = "Lists all venues"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tables", "-t", action="store_true",
            help="Display tables associated with a venue"
        )

    def handle(self, *args, **options):
        venues = Venue.objects.all()
        truncator = Truncator

        for venue in venues:
            truncator = Truncator(venue.description)

            self.stdout.write(
                f"id:{venue.id} Name:{venue.name} Description:{truncator.words(5)}"
            )

            if options["tables"]:
                self.stdout.write("Tables(number:seats):")
                if venue.tables.all():
                    tables = []
                    for table in venue.tables.all():
                        tables.append(f"{table.number}:{table.seats}")
                    self.stdout.write("\n".join(tables))
                else:
                    self.stdout.write("No tables")