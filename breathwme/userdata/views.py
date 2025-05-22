from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Userdata
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Userdata
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Userdata

@login_required
def upload_userdata(request):
    user_data, created = Userdata.objects.get_or_create(user=request.user)  # Fetch or create new data for the user

    if request.method == "POST":
        name = request.POST.get("name")
        date_of_birth = request.POST.get("date_of_birth")
        city = request.POST.get("city")
        country = request.POST.get("country")
        hobby = request.POST.get("hobby")
        favourite_artist = request.POST.get("favourite_artist")
        goal = request.POST.get("goal")
        profile_image = request.FILES.get("profile_image")  # Get uploaded file

        # Check if required fields are filled
        if not name or not city or not country:
            messages.error(request, "Name, City, and Country are required fields.")
            return render(request, "user/upload_userdata.html", {"user_data": user_data})  # Stay on form if error

        try:
            # Update existing user data
            user_data.name = name
            user_data.date_of_birth = date_of_birth
            user_data.city = city
            user_data.country = country
            user_data.hobby = hobby
            user_data.favourite_artist = favourite_artist
            user_data.goal = goal
            if profile_image:  # Only update profile image if a new one is uploaded
                user_data.profile_image = profile_image
            
            user_data.save()  # Save updates
            
            messages.success(request, "User data updated successfully!" if not created else "User data uploaded successfully!")
            return redirect("profile")  # Redirect only if successful
        
        except Exception as e:
            messages.error(request, f"Error: {e}")  # Show error message

    return render(request, "user/upload_userdata.html", {"user_data": user_data})  # Pass existing data to form



# For User Settings log ----------------------------------------------------------------------------------------------------------------
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import UserSettingsPreference
from django.views.decorators.http import require_POST
from django.db.models import F

@login_required
@require_POST
def update_setting(request):
    data = json.loads(request.body)
    field = data.get('field')
    value = data.get('value')

    allowed_fields = ['email_notification', 'push_notification', 'visibility', 'data_access', 'activity_access']
    if field not in allowed_fields:
        return JsonResponse({'error': 'Invalid field'}, status=400)

    updated = UserSettingsPreference.objects.filter(user=request.user).update(**{field: value})
    if not updated:
        return JsonResponse({'error': 'Settings preference does not exist'}, status=404)

    return JsonResponse({'success': True})
