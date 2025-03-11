import datetime
from django.utils.timezone import now
from .models import UserActivity

class TrackUserTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            start_time = now()
            response = self.get_response(request)
            end_time = now()
            duration = end_time - start_time

            activity, _ = UserActivity.objects.get_or_create(user=request.user, date=now().date())
            activity.total_time_spent += duration
            activity.save()

            return response
        else:
            return self.get_response(request)
