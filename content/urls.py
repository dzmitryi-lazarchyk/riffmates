from django.urls import path

from content import views

app_name = "content"

urlpatterns = [
    path("comment/", views.comment, name="comment"),
    path("comment_accepted/", views.comment_accepted, name="comment_accepted"),
]
