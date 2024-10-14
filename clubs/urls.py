from django.urls import path


from clubs import views

app_name = "clubs"

urlpatterns = [
    path('member/<int:member_id>', views.member, name="member"),
    path('members/', views.members, name="members"),
    path('club/<int:club_id>', views.club, name="club"),
    path('clubs/', views.clubs, name="clubs"),
    path('venues/', views.venues, name="venues"),
    path('restricted_page/', views.restricted_page, name="restricted_page"),
    path('member_restricted/<int:member_id>', views.member_restricted, name="member_restricted"),
]