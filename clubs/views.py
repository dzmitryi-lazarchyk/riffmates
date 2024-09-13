import datetime

from django.shortcuts import render, get_object_or_404

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

