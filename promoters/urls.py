from django.urls import path

from . import views

app_name = "promoters"

urlpatterns = [
    path("promoters/", views.promoters, name="promoters"),
    path("partial_promoters/", views.partial_promoters, name="partial_promoters")
]
