from datetime import datetime, date

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from clubs.models import Member, Club, Venue, Table, UserProfile

class DecadeListFilter(admin.SimpleListFilter):
    title = 'Decade born'
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        result = []
        this_year = datetime.today().year
        this_decade = (this_year // 10) * 10
        start = this_decade-10
        for year in range(start, start-100, -10):
            result.append((str(year), f"{year}-{year+9}"))

        return result

    def queryset(self, request, queryset):
        start = self.value()
        if start is None:
            return queryset

        start = int(start)
        result = queryset.filter(
            date_of_birth__gte=date(start, 1, 1),
            date_of_birth__lte=date(start+9, 12, 31)
        )

        return result


class MembershipInline(admin.TabularInline):
    model = Club.members.through



@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name",
                    "calculate_years", "show_weekday",
                    "show_clubs",)
    search_fields = ("first_name", "last_name")
    list_filter = (DecadeListFilter, )
    inlines = [MembershipInline,]

    def show_weekday(self, obj):
        # Fetch weekday of artict's birth
        return obj.date_of_birth.strftime("%A")

    show_weekday.short_description = "Birth weekday"

    def show_clubs(self, obj):
        clubs = obj.club_set.all()
        clubs_count = len(clubs)
        if clubs_count == 0:
            result = "<i>None</i>"
        else:
            # Show changelist link for 3 first member's clubs
            result = []
            clubs_url = reverse("admin:clubs_club_changelist")
            for club in clubs[:3]:
                html = f'<a href="{clubs_url}?id={club.id}">{club.name}</a>'
                result.append(html)
            if clubs_count > 3:
                # Show changelist link of all member's clubs
                parm = "?id__in=" + ",".join([str(club.id) for club in clubs])
                result.append(f'<a href="{clubs_url+parm}">...</a>')
            result = ",".join(result)

        return format_html(result)
    show_clubs.short_description = "Clubs"

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ["name", "show_members"]
    inlines = [MembershipInline, ]
    exclude = ["members"]

    search_fields = ["name", "members__last_name", "members__first_name"]

    def show_members(self, obj):
        members = obj.members.all()
        clubs_count = len(members)
        if clubs_count == 0:
            result = "<i>None</i>"
        else:
            # Show changelist link for 10 first club's members
            result = []
            members_url = reverse("admin:clubs_member_changelist")
            for member in members[:3]:
                html = (f'<a href="{members_url}'
                        f'?id={member.id}">{member.first_name} {member.last_name}</a>')
                result.append(html)
            if clubs_count > 3:
                # Show changelist link of all club's members
                parm = "?id__in=" + ",".join([str(club.id) for club in members])
                result.append(f'<a href="{members_url + parm}">...</a>')
            result = ",".join(result)

        return format_html(result)
    show_members.short_description = "Members"


class TablesInline(admin.TabularInline):
    model = Table
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "show_tables"]
    inlines = [TablesInline, ]
    search_fields = ["name"]
    list_filter = ["tables__seats"]

    def show_tables(self, obj):
        tables = obj.tables.all()
        tables_url = reverse("admin:clubs_table_changelist")
        result = []
        for t in tables:
            html = f'<a href="{tables_url}?id={t.id}">{t.number}({t.seats})</a>'
            result.append(html)
        return format_html(",".join(result))
    show_tables.short_description = "Tables(seats)"

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["number", "seats", "venue"]
    search_fields = ["seats", "venue"]

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
