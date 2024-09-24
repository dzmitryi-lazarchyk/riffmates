import datetime

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from clubs.models import Member, Club

from datetime import date
def member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    # Calculate years
    birth = member.date_of_birth
    now = datetime.date.today()
    years = now.year - birth.year - ((now.month, now.day) < (birth.month, birth.day))

    data = {"member": member,
            "years": years}

    return render(request, "member.html", data)

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
