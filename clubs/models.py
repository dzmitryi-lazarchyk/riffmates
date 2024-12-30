import datetime

from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_login_failed
from django.utils.text import slugify


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField()
    description = models.TextField(blank=True)
    picture = models.ImageField(blank=True, null=True)

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
    description = models.TextField(blank=True)
    picture = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"Venue(id={self.id}, name={self.name})"

    @property
    def slug(self):
        slug = slugify(self.name) + "-" + str(self.id)
        return slug


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


# Create UserProfile when User is created
@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    if kwargs['created'] and not kwargs['raw']:
        user = kwargs['instance']
        try:
            # Double check UserProfile doesn't exist already
            # (admin might create it before the signal fires)
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # No UserProfile exists for this user, create one
            UserProfile.objects.create(user=user)


# Login failed signal
@receiver(user_login_failed)
def track_login_failure(sender, **kwargs):
    username = kwargs['credentials']['username']
    url_and_params = lambda request: request.path + '?next=' + request.GET['next'][1:] \
        if request.GET else request.path
    url = url_and_params(request=kwargs['request'])

    print(f"LOGIN Failure by {username} for {url}")
