from django.db import models
from django.core.validators import MinValueValidator

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField()

    def __str__(self):
        return f'Member(id={self.id}, last_name={self.last_name})'

class Club(models.Model):
    name = models.CharField(max_length=20)
    members = models.ManyToManyField(Member)

    def __str__(self):
        return f"Club(id={self.id}, name={self.name})"

class Venue(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Venue(id={self.id}, name={self.name})"

class Table(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(1)])
    seats = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='tables')

    def __str__(self):
        return f"Table(id={self.id}, number={self.number})"