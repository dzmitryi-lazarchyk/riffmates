def get_page(request, paginator):
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1
    if page_num < 1:
        page_num = 1
    page_obj = paginator.get_page(page_num)

    return page_obj


def get_items_per_page(request, default):
    # Determine number of items per page, disallowing <1 and >50
    try:
        per_page = int(request.GET.get("per_page", default))
    except ValueError:
        per_page = 1
    if per_page < 1:
        per_page = default
    elif per_page > 50:
        per_page = 50
    return per_page
