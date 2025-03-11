from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserActivity
from django.utils.timezone import now

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserActivity
from django.utils.timezone import now

@login_required
def user_dashboard(request):
    today_activity = UserActivity.objects.filter(user=request.user, date=now().date()).first()
    
    formatted_time = "No activity recorded for today."
    
    if today_activity and today_activity.total_time_spent:
        total_seconds = int(today_activity.total_time_spent.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        formatted_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    
    return render(request, 'activity/activity.html', {'formatted_time': formatted_time})
