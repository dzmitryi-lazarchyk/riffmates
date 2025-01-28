from time import sleep

from django.core.paginator import Paginator
from django.shortcuts import render, reverse, resolve_url

from .models import Promoter
from utils.pagination import get_page, get_items_per_page

def promoters(request):
    # print(request.GET.get("page"))
    return render(request, "promoters.html")

def partial_promoters(request):
    all_promoters = Promoter.objects.all().order_by("full_name")
    per_page = get_items_per_page(request, 3)
    paginator = Paginator(all_promoters, per_page)

    page_obj = get_page(request, paginator)
    data = {
        'pagination_url': reverse("promoters:partial_promoters"),
        'promoters': page_obj.object_list,
        'page': page_obj,
        'per_page': per_page,
    }
    return render(request, "partials/promoters.html",
                  data)
