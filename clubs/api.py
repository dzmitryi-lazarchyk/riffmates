from typing import Optional

from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.text import slugify

from ninja import Router, ModelSchema, Field, FilterSchema, Query

from .models import Venue, Table, Club, Member
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

@router.get("/venue/{int:venue_id}/",
            response=VenueOut,
            url_name="fetch_venue")
def fetch_venue(request, venue_id: int):
    venue = get_object_or_404(Venue, id=venue_id)
    return venue

@router.put("/venue/{int:venue_id}/", response=VenueOut, auth=[api_key_header, api_key_querry])
def update_venue(request, venue_id: int, payload: VenueIn):
    data = payload.dict()
    data_tables = data['tables']
    data.pop('tables')
    venue = Venue.objects.filter(id=venue_id)
    venue.update(**data)
    venue = venue[0]
    tables = Table.objects.filter(venue=venue)
    if data_tables:
        for data_table in data_tables:
            try:
                table = tables.get(number=data_table['number'])
                data_table.pop('number')
                for key, value in data_table.items():
                    setattr(table, key, value)
                table.save()
            except Table.DoesNotExist:
                Table.objects.create(venue=venue,
                                     number=data_table['number'],
                                     seats=data_table['seats'])

    return venue

@router.delete("/venue/{int:venue_id}", auth=[api_key_header, api_key_querry])
def delete_venue(request, venue_id:int):
    venue = get_object_or_404(Venue, id=venue_id)
    venue.delete()

    return {"success": True}

class MemberSchema(ModelSchema):
    age: int = Field(None, alias="calculate_years")
    class Meta:
        model = Member
        fields = ["first_name", "last_name",
                  "date_of_birth", "description"]
class ClubOut(ModelSchema):
    members: list[MemberSchema] = Field()
    class Meta:
        model = Club
        fields = ["name"]
@router.get("/clubs/", response=list[ClubOut])
def get_clubs(request):
    clubs = Club.objects.all()
    return clubs