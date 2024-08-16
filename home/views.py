import json
from datetime import date, timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def credits(request):
    content = 'Dzmitryi Lazarchyk\nSample name'

    return HttpResponse(content, content_type='text/plain')

def about(request):
    content = ['<!doctype html>',
               '<html lang="en">',
               '<head>',
               '<title>Foodmates about page</title>',
               '</head>',
               '<body>',
               '    <h1>About page</h1>',
               '    <p>This is an "about" page of Foodmates. Here foodmate can find a foodmate.',
               '    Foodmates can form a club. Find your next venue.</p>'
               '</body>',
               ]
    content = "\n".join(content)

    return HttpResponse(content)

def version_info(request):
    data = {
        'version': '0.0.1',
    }


    return JsonResponse(data)

def news(request):
    context = {
        'news': [
            "FoodMates now has a news page!",
            "FoodMates has its first web page!",
        ],
    }

    return render(
        request,
        template_name="news2.html",
        context=context
    )

def news_advanced(request):
    today = date.today()
    before1 = today - timedelta(days=1)
    before2 = today - timedelta(days=2)

    data = {
        "news": [(today, "News from today"),
                 (before1, "News from yesterday"),
                 (before2, "News from the day before yesterday"),]
    }

    return render(
        request,
        template_name="news_adv.html",
        context=data,
    )
