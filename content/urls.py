from django.urls import path

from content import views

app_name = "content"

urlpatterns = [
    path("comment/", views.comment, name="comment"),
    path("comment_accepted/", views.comment_accepted, name="comment_accepted"),
    path("list_ads/", views.list_ads, name="list_ads"),
    path("seeking_ad/", views.seeking_ad, name="seeking_ad"),
]
