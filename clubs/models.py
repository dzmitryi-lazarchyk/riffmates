import datetime

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField()

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["last_name", "first_name"])]
    def __str__(self):
        return f'Member(id={self.id}, last_name={self.last_name})'

    def calculate_years(self):
        # Calculate years
        birth = self.date_of_birth
        now = datetime.date.today()
        years = now.year - birth.year - ((now.month, now.day) < (birth.month, birth.day))

        return years
    calculate_years.short_description = "Years Old"



class Club(models.Model):
    name = models.CharField(max_length=20)
    members = models.ManyToManyField(Member)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"Club(id={self.id}, name={self.name})"

class Venue(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]
    def __str__(self):
        return f"Venue(id={self.id}, name={self.name})"

class Table(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
    seats = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='tables')

    class Meta:
        unique_together = [["number", "venue"]]
        ordering = ["number"]

    def __str__(self):
        return f"Table(id={self.id}, number={self.number})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_profile = models.OneToOneField(Member, blank=True, null=True, on_delete=models.SET_NULL)
    venues_controlled = models.ManyToManyField(Venue, blank=True)
