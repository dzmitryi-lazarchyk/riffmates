"""
URL configuration for foodmates project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from home import views as home_views

from ninja import NinjaAPI
from home.api import router as home_router
from promoters.api import router as promoter_router

api = NinjaAPI(version="1.0")
api.add_router("/home/", home_router)
api.add_router("/promoters/", promoter_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('credits/', home_views.credits, name="credits"),
    path('about/', home_views.about),
    path('version/', home_views.version_info),
    path('news/', home_views.news, name="news"),
    path('adv_news/', home_views.news_advanced, name="news_advanced"),
    path('clubs/', include("clubs.urls", namespace='clubs')),
    path('content/', include("content.urls", namespace='content')),
    path('api/v1/', api.urls),
    path('', home_views.home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)