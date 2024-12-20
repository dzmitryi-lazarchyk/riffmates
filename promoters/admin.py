from django.contrib import admin

from promoters.models import Promoter

@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ["id", "common_name", "full_name"]
