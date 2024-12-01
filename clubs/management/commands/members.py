from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from clubs.models import Member
class Command(BaseCommand):
    help = "Lists all members"

    def add_arguments(self, parser):
        parser.add_argument("--last_name", "-l",
            help=(
                "Query members whose last name is greater than or equal"
                " to this value. Note this is case sensitive."
            )
        )
        parser.add_argument("--first_name", "-f",
            help=(
                "Query members whose first name is greater than or equal"
                " to this value. Note this is case sensitive."
            )
        )
        parser.add_argument("--date_of_birth", "-d",
            help=(
                "Query musicians "
                "whose birth date is greater than or equal to this value. "
                "Date must be given in YYYY-MM-DD format."
            )
        )
    def handle(self, *args, **options):
        members = Member.objects.all()
        if options['last_name']:
            members = members.filter(
                last_name__gte=options['last_name']
            )
        if options['first_name']:
            members = members.filter(
                last_name__gte=options['first_name']
            )
        if options['date_of_birth']:
            try:
                date_of_birth = datetime.strptime(
                    options['date_of_birth'], "%Y-%m-%d"
                )
            except ValueError:
                raise CommandError(
                    "Birth date must be provided in YYYY-MM-DD format"
                )
            members = members.filter(date_of_birth__gte=date_of_birth)

        for member in members:
            self.stdout.write(
                f"{member.last_name} {member.first_name}"
                f"({member.date_of_birth.strftime("%Y-%m-%d")})"
            )



