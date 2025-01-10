from django.urls import path

from ninja import NinjaAPI
from home.api import router as home_router
from promoters.api import router as promoters_router
from clubs.api import router as clubs_router

from api import views

api = NinjaAPI(version="1.0")
api.add_router("/home/", home_router)
api.add_router("/promoters/", promoters_router)
api.add_router("/clubs/", clubs_router)

app_name = "api"

urlpatterns = [
    path("v1/", api.urls),
    path("keys/", views.keys, name="keys"),
    path("delete_key/<int:key_id>/", views.delete_key, name="delete_key")
]
