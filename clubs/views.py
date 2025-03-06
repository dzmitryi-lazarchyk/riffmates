import urllib.parse
from datetime import date

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import Greatest
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity

from clubs.forms import VenueForm, MemberForm
from clubs.models import Member, Club, Venue
from utils.pagination import get_page, get_items_per_page


@login_required
def member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.controller = False
    if request.user.is_staff:
        member.controller = True
    if hasattr(request.user, "userprofile"):
        if request.user.userprofile.member_profile:
            member.controller = request.user.userprofile.member_profile.id == member_id
    years = member.calculate_years()

    data = {"member": member, "years": years}

    return render(request, "member.html", data)


@login_required
def add_edit_member(request, member_id=0):
    add, edit = member_id == 0, member_id != 0
    member = None
    if add and request.user.userprofile.member_profile:
        add, edit = edit, add
        member_id = request.user.userprofile.member_profile.id
    if edit:
        member = get_object_or_404(Member, id=member_id)
        if request.user.userprofile.member_profile:
            if not request.user.userprofile.member_profile.id == member_id:
                raise Http404("You can only edit your own member profile info.")
        elif (not request.user.is_staff) and (not request.user.is_superuser):
            raise Http404("You can only edit your own member profile info.")

    if request.method == "GET":
        if add:
            form = MemberForm()
        else:
            form = MemberForm(instance=member)

    else:  # POST
        if add:
            member = Member.objects.create(date_of_birth=date(1990, 1, 1))
        form = MemberForm(request.POST, request.FILES, instance=member)

        if form.is_valid():
            member = form.save()
            if not request.user.is_staff and add:
                user_profile = request.user.userprofile
                user_profile.member_profile = member
                user_profile.save()
            return redirect("clubs:members")

    data = {'form': form, 'member': member, }

    return render(request, "add_edit_member.html", data)


def members(request):

    if request.htmx:
        template_name = "partials/members_results.html"
    else:
        template_name = "members.html"

    members = []
    search_text = request.GET.get("search_text", "")

    if search_text:
        search_text = urllib.parse.unquote(search_text)
        search_text = search_text.strip()
        # DEBUG with sqlite3
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            if search_text:
                parts = search_text.split()

                q = (Q(first_name__istartswith=parts[0]) |
                     Q(last_name__istartswith=parts[0]))
                for part in parts[1:]:
                    q |= (Q(first_name__istartswith=part) |
                          Q(last_name__istartswith=part))

                members = Member.objects.filter(q)
        # DEBUG False with PostgreSQL and trigram
        elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            members = Member.objects.annotate(
                similarity=Greatest(
                    TrigramSimilarity('first_name', search_text),
                    TrigramSimilarity('last_name', search_text)
                )
            ).filter(similarity__gte=0.1).order_by('-similarity')
    else:
        members = Member.objects.all().order_by("last_name")
    print(request.GET)
    per_page = get_items_per_page(request, 1)
    paginator = Paginator(members, per_page)

    page_obj = get_page(request, paginator)
    data = {'members': page_obj.object_list,
            'page': page_obj,
            'per_page': per_page,
            "search_text": search_text,
            }
    return render(request, template_name, data)


def club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    data = {'club': club}

    return render(request, "club.html", data)


def clubs(request):
    all_clubs = Club.objects.all().annotate(count=Count('members')).order_by('count')
    per_page = get_items_per_page(request, 5)
    paginator = Paginator(all_clubs, per_page)

    page_obj = get_page(request, paginator)

    data = {'clubs': page_obj.object_list, 'page': page_obj, 'per_page': per_page, }

    return render(request, "clubs.html", data)


def venues(request):
    all_venues = Venue.objects.order_by('name')
    profile = getattr(request.user, "userprofile", None)
    if profile:
        for venue in all_venues:
            # Mark as controlled if logged user is
            # associated with the venue
            venue.controlled = profile.venues_controlled.filter(id=venue.id).exists()
    else:
        for venue in all_venues:
            venue.controlled = False
    per_page = get_items_per_page(request, 5)
    paginator = Paginator(all_venues, per_page)

    page_obj = get_page(request, paginator)

    data = {'venues': page_obj.object_list, 'page': page_obj}

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
    data = {'title': 'Restricted Page', 'content': '<h1>You are logged in.</h1>'}

    return render(request, "general.html", data)


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
    data = {'title': 'Member Restricted', 'content': content, }
    return render(request, "general.html", data)


@login_required
def add_edit_venue(request, venue_id=0):
    add, edit = venue_id == 0, venue_id != 0
    if edit:
        venue = get_object_or_404(Venue, id=venue_id)
        if not request.user.userprofile.venues_controlled.filter(id=venue_id).exists():
            raise Http404("You can only edit controlled venues.")

    if request.method == "GET":
        if add:
            form = VenueForm()
            venue = None
        else:
            form = VenueForm(instance=venue)

    else:  # POST
        if add:
            venue = Venue.objects.create()

        form = VenueForm(request.POST, request.FILES, instance=venue)

        if form.is_valid():
            venue = form.save()

            # Add the venue to user's profile
            request.user.userprofile.venues_controlled.add(venue)
            return redirect("clubs:venues")

    # GET or form is not valid
    data = {'form': form, 'venue': venue, }

    return render(request, "add_edit_venue.html", data)

def search_members(request):
    search_text = request.GET.get("search_text", "")
    print(request.GET)
    search_text = urllib.parse.unquote(search_text)
    search_text = search_text.strip()
    members = []

    # DEBUG with sqlite3
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        if search_text:
            parts = search_text.split()

            q = (Q(first_name__istartswith=parts[0]) |
                 Q(last_name__istartswith=parts[0]))
            for part in parts[1:]:
                q |= (Q(first_name__istartswith=part) |
                      Q(last_name__istartswith=part))

            members = Member.objects.filter(q)
    # DEBUG False with PostgreSQL and trigram
    elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
        if search_text:
            members = Member.objects.annotate(
                similarity=Greatest(
                    TrigramSimilarity('first_name', search_text),
                    TrigramSimilarity('last_name', search_text)
                )
            ).filter(similarity__gte=0.1).order_by('-similarity')

    data = {
        "search_text": search_text,
        "members": members
    }

    return render(request, "partials/members_results.html", data)