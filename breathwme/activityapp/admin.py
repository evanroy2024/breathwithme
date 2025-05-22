from django.contrib import admin
from django.utils.timezone import now
from django.contrib import messages

from .models import PageVisit, DailyUserSummary

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'date', 'duration_seconds')
    actions = ['update_daily_summaries']

    def update_daily_summaries(self, request, queryset):
        url_category_map = {
            '/breathxapp/breathfree': 'breath_free_page',
            '/breathxapp/play': 'breathx_play_page',
            '/breathxapp/view-exercise': 'breath_save_page',
            '/testapp/exercise': 'breathing_beats_page',
            # Add more mappings if needed
        }

        users_dates = queryset.values_list('user', 'date').distinct()
        count = 0

        for user, date in users_dates:
            totals = {field: 0 for field in url_category_map.values()}
            totals['course_page'] = 0  # If you want to sum this too

            visits = PageVisit.objects.filter(user=user, date=date)
            for visit in visits:
                for prefix, field in url_category_map.items():
                    if visit.url.startswith(prefix):
                        totals[field] += visit.duration_seconds
                        break

            summary, created = DailyUserSummary.objects.get_or_create(user_id=user, date=date)
            for field, total_seconds in totals.items():
                setattr(summary, field, total_seconds)
            summary.save()
            count += 1


        self.message_user(request, f"Updated daily summaries for {count} user/day combinations.")

    update_daily_summaries.short_description = "Update Daily Summaries for selected PageVisits"

# Register DailyUserSummary normally
admin.site.register(DailyUserSummary)
