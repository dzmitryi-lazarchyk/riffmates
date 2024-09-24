from django.urls import path

import clubs.views

from clubs import views

app_name = "clubs"

urlpatterns = [
    path('member/<int:member_id>', views.member, name="member"),
    path('members/', views.members, name="members"),
    path('club/<int:club_id>', views.club, name="club"),
    path('clubs/', views.clubs, name="clubs"),
    path('venues/', views.venues, name="venues"),
]