from django.urls import path

import clubs.views

from clubs import views

app_name = "clubs"

urlpatterns = [
    path('member/<int:member_id>', views.member, name="member"),
    path('members/', views.members, name="members"),
]