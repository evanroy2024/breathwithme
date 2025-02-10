from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Userdata

@login_required
def upload_userdata(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date_of_birth = request.POST.get("date_of_birth")
        city = request.POST.get("city")
        country = request.POST.get("country")
        hobby = request.POST.get("hobby")
        favourite_artist = request.POST.get("favourite_artist")
        goal = request.POST.get("goal")
        profile_image = request.FILES.get("profile_image")  # Get the uploaded file

        # Save data to the Userdata model
        Userdata.objects.create(
            user=request.user,
            name=name,
            date_of_birth=date_of_birth,
            city=city,
            country=country,
            hobby=hobby,
            favourite_artist=favourite_artist,
            goal=goal,
            profile_image=profile_image,
        )
        return redirect("profile")  # Redirect to a success page or display a success message
    
    return render(request, "user/upload_userdata.html")
