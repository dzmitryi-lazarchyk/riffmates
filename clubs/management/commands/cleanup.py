import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from clubs.models import Member, Venue


class Command(BaseCommand):
    help = "Removes uploaded files not owned by Member or Venue"

    def add_arguments(self, parser):
        parser.add_argument(
            "--show",
            "-s",
            action="store_true",
            help="shows files to be removed but doesn't remove them"
        )

    def handle(self, *args, **options):

        model_set = set()
        for member in Member.objects.all():
            if member.picture:
                model_set.add(Path(member.picture.path))
        for venue in Venue.objects.all():
            if venue.picture:
                model_set.add(Path(venue.picture.path))

        file_set = set(settings.MEDIA_ROOT.glob("**/*"))

        orphaned = file_set.difference(model_set)

        if not orphaned:
            self.stdout.write("No orphaned files")
            sys.exit()
        if options['show']:
            self.stdout.write(f"Orphaned files:({len(orphaned)})")
            for path in orphaned:
                if path.is_file():
                    self.stdout.write("  " + str(path))
        else:
            self.stdout.write(f"Removing files:({len(orphaned)})")
            for path in orphaned:
                if path.is_file():
                    self.stdout.write("  " + str(path))

                    path.unlink()
