from django.urls import path
from . import views

app_name = "api_manage"

urlpatterns = [
    path("keys/", views.keys, name="keys"),
    path("delete_key/<int:key_id>/", views.delete_key, name="delete_key")
]