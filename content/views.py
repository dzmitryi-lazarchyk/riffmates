from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

from content.forms import CommentForm, SeekingAdForm
from content.models import SeekingAd, MemberClubChoice
def comment(request):
    if request.method == 'GET':
        form = CommentForm()

    elif request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]

            message = f"""\
            Receieved comment from {name}\n\n{comment}
            """
            send_mail("Recevied comment", message,
                      settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER],
                      fail_silently=False)
            return redirect("content:comment_accepted")

    data = {
        "form": form,
    }
    return render(request, "comment.html", data)

def comment_accepted(request):
    data = {
        "content": """
        <h1> Comment Accepted</h1>
        <p> Thanks for submitting a comment to <i>FoodMates</i> </p>
        """

    }

    return render(request, "general.html", data)

def list_ads(request):
    data = {'seeking_member': SeekingAd.objects.filter(
        seeking=MemberClubChoice.MEMBER),
            'seeking_band': SeekingAd.objects.filter(
        seeking=MemberClubChoice.CLUB)
    }

    return render(request, "list_ads.html", data)


@login_required
def seeking_ad(request, ad_id=0):
    user_is_staff = False
    if not ad_id == 0:
        user_is_staff = request.user.is_staff
    if request.method == 'GET':
        if ad_id == 0:
            form = SeekingAdForm()
        else:
            ad_kwargs = {"id": ad_id}
            if not user_is_staff:
                ad_kwargs["owner"] = request.user
            ad = get_object_or_404(SeekingAd, **ad_kwargs)
            form = SeekingAdForm(instance=ad)
    else:  # POST
        if ad_id == 0:
            form = SeekingAdForm(request.POST)
        else:
            ad_kwargs = {"id": ad_id}
            if not user_is_staff:
                ad_kwargs["owner"] = request.user
            ad = get_object_or_404(SeekingAd, **ad_kwargs)
            form = SeekingAdForm(request.POST, instance=ad)
        if form.is_valid():
            if not user_is_staff:
                ad = form.save(commit=False)
                ad.owner = request.user
                ad.save()
            else:
                ad = form.save()

            return redirect("content:list_ads")

    # GET or form is not valid
    data = {
        "form": form,
    }

    return render(request, "seeking_ad.html", data)


