from django.shortcuts import render, redirect
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
def seeking_ad(request):
    if request.method == 'GET':
        form = SeekingAdForm()
    else:
        form = SeekingAdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()

            return redirect("content:list_ads")

    # GET or form is not valid
    data = {
        "form": form,
    }

    return render(request, "seeking_ad.html", data)
