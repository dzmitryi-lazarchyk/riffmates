from django.http import HttpResponse

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
