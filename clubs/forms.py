from django import forms
from clubs.models import Venue

VenueForm = forms.modelform_factory(
    Venue,
    fields=["name", "description", "picture"]
)