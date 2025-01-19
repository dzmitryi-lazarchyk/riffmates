from typing import Optional

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

from ninja import Router, ModelSchema, Field, FilterSchema, Query

from .models import Venue, Table
from api.auth import api_key_header, api_key_querry

router = Router()

class TableSchema(ModelSchema):
    class Meta:
        model = Table
        fields = ["id", "number", "seats"]
class VenueOut(ModelSchema):
    slug: str
    url: str
    tables: list[TableSchema] = Field(...)

    class Meta:
        model = Venue
        fields = ["id", "name", "description",]

    # Slug field implemented as a model's field.
    # You can use the code below alternatively

    # @staticmethod
    # def resolve_slug(obj):
    #     slug = slugify(obj.name) + "-" + str(obj.id)
    #     return slug

    @staticmethod
    def resolve_url(obj):
        url = reverse("api-1.0:fetch_venue", args=[obj.id, ])
        return url

class VenueFilter(FilterSchema):
    name: Optional[str] = Field(None,
                                q=['name__istartswith'])

@router.get("/venue/{venue_id}/",
            response=VenueOut,
            url_name="fetch_venue")
def fetch_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    return venue

@router.get("/venues/",
            response=list[VenueOut])
def venues(request, filters: VenueFilter = Query(...)):
    venues = Venue.objects.all()
    venues = filters.filter(venues)
    return venues

class TableIn(ModelSchema):
    class Meta:
        model = Table
        fields = ['number', 'seats']

class VenueIn(ModelSchema):
    tables: list[TableIn] = []
    class Meta:
        model = Venue
        fields = ['name', 'description']




@router.post("/venue/", response=VenueOut, auth=[api_key_header, api_key_querry])
def create_venue(request, payload: VenueIn):
    data = payload.dict()
    data_tables = data['tables']
    data.pop('tables')
    venue = Venue.objects.create(**data)
    if data_tables:
        for data_table in data_tables:
            Table.objects.create(venue=venue,
                                 number=data_table['number'],
                                 seats=data_table['seats'])

    return venue
