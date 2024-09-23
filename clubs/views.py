import datetime

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
def members(request):
    all_members = Member.objects.all().order_by("-last_name")
    per_page = _get_items_per_page(request, 5)

    page_num = request.GET.get('page')
    paginator = Paginator(all_members, per_page)

    try:
        page_obj = paginator.get_page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    data = {
        'members': page_obj.object_list,
        'page': page_obj,
        'per_page': per_page,
    }

    return render(request, "members.html", data)

