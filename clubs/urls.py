from django.urls import path


from clubs import views

app_name = "clubs"

urlpatterns = [
    path('member/<int:member_id>/', views.member, name="member"),
    path('members/', views.members, name="members"),
    path('club/<int:club_id>/', views.club, name="club"),
    path('clubs/', views.clubs, name="clubs"),
    path('venues/', views.venues, name="venues"),
    path('restricted_page/', views.restricted_page, name="restricted_page"),
    path('member_restricted/<int:member_id>/', views.member_restricted, name="member_restricted"),
    path('edit_venue/', views.add_edit_venue, name="add_venue"),
    path('edit_venue/<int:venue_id>/', views.add_edit_venue, name="edit_venue"),
    path('add_edit_member/', views.add_edit_member, name="add_member"),
    path('add_edit_member/<int:member_id>/', views.add_edit_member, name="edit_member"),
    path('search_members/', views.search_members, name="search_members"),
]