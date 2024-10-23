import datetime

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test

from clubs.models import Member, Club, Venue, UserProfile

from datetime import date

def _get_items_per_page(request, default):
    # Determine number of items per page, disallowing <1 and >50
    per_page = int(request.GET.get("per_page", default))
    if per_page < 1:
        per_page = default
    elif per_page > 50:
        per_page = 50
    return per_page

def _get_page(request, paginator):
    page_num = int(request.GET.get('page', 1))
    if page_num < 1:
        page_num = 1
    page_obj = paginator.get_page(page_num)

    return page_obj

def member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    years = member.calculate_years()

    data = {"member": member,
            "years": years}

    return render(request, "member.html", data)


def members(request):
    all_members = Member.objects.all().order_by("last_name")
    per_page = _get_items_per_page(request, 5)
    paginator = Paginator(all_members, per_page)

    page_obj = _get_page(request, paginator)

    data = {
        'members': page_obj.object_list,
        'page': page_obj,
        'per_page': per_page,
    }

    return render(request, "members.html", data)


def club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    data = {'club': club}

    return render(request, "club.html", data)


def clubs(request):
    all_clubs = Club.objects.all().annotate(count=Count('members')).order_by('count')
    per_page = _get_items_per_page(request, 5)
    paginator = Paginator(all_clubs, per_page)

    page_obj = _get_page(request, paginator)

    data = {
        'clubs': page_obj.object_list,
        'page': page_obj,
        'per_page': per_page,
    }

    return render(request, "clubs.html", data)

def venues(request):
    all_venues = Venue.objects.all().order_by('name')
    per_page = _get_items_per_page(request, 5)
    paginator = Paginator(all_venues, per_page)

    page_obj = _get_page(request, paginator)

    data = {'venues': page_obj.object_list,
            'page': page_obj}

    return render(request, "venues.html", data)

def user_associated_with_venue(user):
    try:
        return user.userprofile.venues_controlled.count() > 0
    except AttributeError:
        return False


@user_passes_test(user_associated_with_venue)
def venues_restricted(request):
    venues(request)

@login_required
def restricted_page(request):
    data = {
        'title': 'Restricted Page',
        'content': '<h1>You are logged in.</h1>'
    }

    return render(request,
                  "general.html",
                  data)

@login_required
def member_restricted(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    profile = request.user.userprofile
    allowed = False

    if profile.member_profile.id == member_id:
        allowed = True
    else:
        # User is not this member. Check if they're food-mates
        member_clubs = member.club_set.all()
        for club in member_clubs:
            if profile.member_profile in club.members.all():
                allowed = True
                break

    if not allowed:
        raise Http404("Permission denied.")
    content = f"""
        <h1>Member Page: {member.last_name}</h1>
"""
    data = {
        'title': 'Member Restricted',
        'content': content,
    }
    return render(request, "general.html", data)