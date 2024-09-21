import datetime

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from clubs.models import Member

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

def members(request):
    all_members = Member.objects.all().order_by("-last_name")
    paginator = Paginator(all_members, 2)

    page_num = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    data = {
        'members': page_obj.object_list,
        'page': page_obj,
    }

    return render(request, "members.html", data)