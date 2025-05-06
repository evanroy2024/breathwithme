from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def main_page(request):
    return render(request, 'mainapp/index.html')

# Dark to light theme code here start 
def toggle_theme(request):
    # Get the current theme (default to 'light' if not set)
    current_theme = request.session.get('theme', 'light')

    # Toggle the theme
    new_theme = 'dark' if current_theme == 'light' else 'light'

    # Save the new theme in the session
    request.session['theme'] = new_theme

    return JsonResponse({'theme': new_theme})
# Dark to light theme code here End



def theme1(request):
    return render(request, 'mainapp/theme1.html')

# Starting of Auth here ------------------------------------------------------------------
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from referal.models import ReferralLink, DigitalCoin  # Import referral & coin models

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))  # Ensure OTP is stored as a string

# Register view with referral code support

def register(request):
    referral_code = request.GET.get("ref")  # Get referral code from URL

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # Generate OTP and save in session
        otp = generate_otp()
        request.session["otp"] = otp

        # Save referral code in session (if provided)
        if referral_code:
            request.session["referral_code"] = referral_code  

        # Send OTP email
        send_mail(
            "Your OTP Code",
            f"Your OTP code is {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Save user data temporarily to session
        request.session["username"] = username
        request.session["email"] = email
        request.session["password"] = password

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect("otp_varify")  # Redirect to OTP verification page

    return render(request, "user/register.html")
# OTP verification view with referral rewards
def otp_varify(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        # Verify OTP
        if entered_otp == str(request.session.get("otp")):  # Ensure string comparison
            username = request.session.get("username")
            email = request.session.get("email")
            password = request.session.get("password")

            # Create new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Initialize user's digital coin balance
            DigitalCoin.objects.get_or_create(user=user, defaults={"amount": 0})

            # Check if referral code was used
            referral_code = request.session.get("referral_code")
            if referral_code:
                try:
                    # Find the user who referred using the referral code
                    referrer = ReferralLink.objects.get(code=referral_code).user
                    digital_coin, created = DigitalCoin.objects.get_or_create(user=referrer)
                    digital_coin.amount += 5  # Reward the referrer with 5 coins
                    digital_coin.save()
                except ReferralLink.DoesNotExist:
                    pass  # Ignore if the referral code does not exist or is invalid

            # Clear session data after successful registration
            request.session.flush()

            messages.success(request, "OTP verified successfully! You can now login.")
            return redirect("signin")

        messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "user/otp.html")
   
def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try to get the user by email, assuming email is used for login
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Authenticate user
        if user and user.check_password(password):  # Check if password matches
            login(request, user)  # Log the user in
            messages.success(request, "You have successfully logged in!")
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'user/signin.html')

def user_logout(request):
    logout(request)
    return redirect('signin')  # Redirect the user to the homepage or any other page

# Ending of Auth here ------------------------------------------------------------------

# Subscriptions go there Start --------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import SubscriptionPlan, Subscription
import paypalrestsdk
from django.conf import settings

# Ensure PayPal configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

# View to display subscription plans
def subscriptions(request):
    plans = SubscriptionPlan.objects.all()  # Fetch all subscription plans from the database
    return render(request, 'subscriptions/subs.html', {'plans': plans})

# Create payment view
def create_payment(request, plan_id):
    # Get the selected plan from the database
    plan = SubscriptionPlan.objects.get(id=plan_id)

    # Create PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/paypal/execute/'),
            "cancel_url": request.build_absolute_uri('/subscriptions/')
        },
        "transactions": [{
            "amount": {
                "total": str(plan.price),
                "currency": "USD"
            },
            "description": plan.name
        }]
    })

    if payment.create():
        # Store payment transaction ID in session to verify on return
        request.session['payment_id'] = payment.id
        request.session['selected_plan_id'] = plan.id  # Store the selected plan ID

        # Redirect to PayPal for approval
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return redirect(approval_url)

    return redirect('subscriptions')  # Redirect back if payment creation fails

# Execute payment after PayPal approval
def execute_payment(request):
    payment_id = request.session.get('payment_id', None)
    payer_id = request.GET.get('PayerID', None)

    if payment_id and payer_id:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            # Payment successful, create subscription record in the database
            plan_id = request.session.get('selected_plan_id')  # Get the selected plan ID
            user = request.user  # Get the logged-in user

            plan = SubscriptionPlan.objects.get(id=plan_id)
            subscription = Subscription(
                user=user,
                plan=plan,
                payment_status='Completed',
                payment_transaction_id=payment.id
            )
            subscription.save()

            # Clear session data
            request.session.pop('payment_id', None)
            request.session.pop('selected_plan_id', None)

            # Redirect to home page or a success page
            return redirect('home')  # Redirect to home after successful subscription

    return redirect('subscriptions')  # Redirect back if payment failed

# Subscriptions go there End --------------------------------------------------------------------------------

# Starting of Home and operations here -----------------------------------------------------------------
from django.shortcuts import render
from userdata.models import Userdata
from django.contrib.auth.decorators import login_required
from .decorators import check_subscription

@check_subscription
@login_required
def home(request):
    userdata = Userdata.objects.filter(user=request.user).first()
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'user/home.html', {'username': username,'userdata': userdata})

from musicapp.models import Playlist
def library(request):
    playlists = Playlist.objects.all()  # Fetch all playlists
    return render(request, 'user/library.html', {'playlists': playlists})

def sleep(request):
    return render(request, 'user/sleep.html')


# Ending of Home and operations here -----------------------------------------------------------------


# Courser go there Start --------------------------------------------------------------------------------

def main_page_course(request):
    return render(request, 'course/mainpage.html')
# Courser go there End --------------------------------------------------------------------------------




# Tracker go there Start --------------------------------------------------------------------------------

def tracker(request):
    return render(request, 'user/tracker.html')
# Tracker go there End --------------------------------------------------------------------------------




# Profile go there Start --------------------------------------------------------------------------------
from django.shortcuts import render
from userdata.models import Userdata
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    # Fetch the current user's data from the Userdata model
    userdata = Userdata.objects.filter(user=request.user).first()
    
    return render(request, 'user/profile.html', {'userdata': userdata})

def language(request):
    return render(request, 'user/language.html')

def sequrity(request):
    return render(request, 'user/sequrity.html')

def user_settings(request):
    return render(request, 'user/settings.html')
# Profile go there End --------------------------------------------------------------------------------




# Custom Features Starts here ------------------------------------------------------------------------
from musicapp.models import MusicTrack

# def music_player(request):
#     tracks = MusicTrack.objects.all()
    
#     # Example: Getting vibration patterns for all tracks
#     vibration_patterns = {track.title: track.get_vibration_pattern() for track in tracks}
    
#     return render(request, 'myapp/music_player.html', {
#         'tracks': tracks,
#         'vibration_patterns': vibration_patterns,
#     })

from django.shortcuts import render
from musicapp.models import MusicTrack, Playlist , Category

def music_player(request):
    # user_playlists = Playlist.objects.filter(user=request.user)
    categories = Category.objects.all()  # Get all categories
    
    selected_playlist_id = request.GET.get("playlist", None)
    selected_category_id = request.GET.get("category", None)

    tracks = MusicTrack.objects.all()  # Default: show all tracks

    if selected_playlist_id and selected_playlist_id != "all":
        selected_playlist = Playlist.objects.get(id=selected_playlist_id, user=request.user)
        tracks = selected_playlist.tracks.all()  

    if selected_category_id and selected_category_id != "all":
        tracks = tracks.filter(category_id=selected_category_id)

    return render(request, 'myapp/music_player.html', {
        'tracks': tracks,
        # 'playlists': user_playlists,
        'categories': categories,
        'selected_playlist': selected_playlist_id
    })


# //////////////////////////////////// SubscriptionPlan CHECK START //////////////////////////////////////
from django.urls import path
from django.shortcuts import render

# View for Subscription Expired Page
def subscription_expired(request):
    userdata = Userdata.objects.filter(user=request.user).first()
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'user/home.html', {'username': username,'userdata': userdata})

# //////////////////////////////////// SubscriptionPlan CHECK End ////////////////////////////////////////
