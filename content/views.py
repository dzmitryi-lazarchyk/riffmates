from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from content.forms import CommentForm
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
