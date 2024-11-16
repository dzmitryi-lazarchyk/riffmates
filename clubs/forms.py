from django import forms
from django.forms.widgets import SelectDateWidget, DateInput

from clubs.models import Venue, Member

VenueForm = forms.modelform_factory(
    Venue,
    fields=["name", "description", "picture"]
)

MemberForm = forms.modelform_factory(
    Member,
    fields=["first_name",
            "last_name",
            "date_of_birth",
            "description",
            "picture"],
    widgets={"date_of_birth": DateInput(attrs={'type': 'date'})}
)
