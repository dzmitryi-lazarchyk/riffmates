from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from clubs.models import Member, Club


class MemberClubChoice(models.TextChoices):
    MEMBER = "M"
    CLUB = "C"


class SeekingAd(models.Model):
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    seeking = models.CharField(max_length=1,
                               choices=MemberClubChoice.choices)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    content = models.TextField()

    class Meta:
        ordering = ["-date",]

    def __str__(self):
        return f"SeekingAd(id={self.id}), seeking={self.seeking}"

    def clean(self):
        if self.seeking == MemberClubChoice.MEMBER:
            if self.club is None:
                raise ValidationError(
                    "Club field is required when seeking a member."
                )
            if self.member is not None:
                raise ValidationError(
                    "Member field should be empty for a club"
                    "seeking a member."
                )
        else:
            if self.member is None:
                raise ValidationError(
                    "Member field is required when seeking a club."
                )
            if self.club is not None:
                raise ValidationError(
                    "Club field should be empty for a member"
                    "seeking a club."
                )

        super().clean()
