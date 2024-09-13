from django.urls import path

import clubs.views

from clubs import views

urlpatterns = [
    path('member/<int:member_id>', views.member, name="member"),
]