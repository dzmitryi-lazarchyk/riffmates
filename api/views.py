from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from typing import Optional

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

from ninja import Router, ModelSchema, Field, FilterSchema, Query

from .models import ApiKey


router = Router()
@login_required
def keys(request):
    user = request.user
    if request.method == "POST":
        full_key, obj = ApiKey.objects.create(user=user)
        messages.add_message(request, messages.WARNING, f"Your new API: {full_key} Store it somewhere save."
                                                     f"You will not be able to see it again.")
    keys = user.api_keys.all()
    data = {"keys": keys}

    return render(request, "api_keys.html", data)

@login_required
def delete_key(request, key_id):
    user = request.user
    key = get_object_or_404(ApiKey, user=user, id=key_id)
    prefix = key.prefix
    key.delete()
    messages.add_message(request, messages.INFO, f"API key {prefix} successfully deleted.")
    return redirect("api:keys")

