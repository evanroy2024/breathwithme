from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def main_page(request):
    return render(request, 'mainapp/index.html')

def app_main_page(request):
    return render(request, 'mainapp/app_main_page.html')

def terms_and_conditions(request):
    return render(request, 'rules/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'rules/privacy_policy.html')

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
    all_plans = SubscriptionPlan.objects.all()

    context = {
        'all_plans': all_plans,
    }
    return render(request, 'mainapp/theme1.html',{'all_plans':all_plans})

# Starting of Auth here ------------------------------------------------------------------
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import datetime


import random
from datetime import datetime  # ✅ Correct import
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from referal.models import DigitalCoin , ReferralLink
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))



# Register view with referral support
def register(request):
    referral_code = request.GET.get("ref")

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

        # Generate OTP and store time
        otp = generate_otp()
        request.session["otp"] = otp
        request.session["otp_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save referral code if provided
        if referral_code:
            request.session["referral_code"] = referral_code

        # -----------------------
        # Send Beautiful HTML Email
        # -----------------------
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 30px; background-color: #f5faff; color: #333;">
            <h2 style="color: #4a90e2;">Welcome to <span style="color:#6e8efb;">Breathe</span> 🌬️</h2>
            <p style="font-size: 16px; margin-top: 20px;">
                We're so glad you've decided to join us on a path to greater calm, clarity, and mindfulness. 💙
            </p>
            <p style="font-size: 16px; margin-top: 10px;">
                To complete your registration and begin your breathing journey, please enter the OTP below:
            </p>

            <div style="text-align: center; margin: 40px 0;">
                <span style="
                    display: inline-block;
                    padding: 20px 40px;
                    font-size: 36px;
                    font-weight: bold;
                    color: #ffffff;
                    background: linear-gradient(135deg, #6e8efb, #a777e3);
                    border-radius: 14px;
                    letter-spacing: 2px;
                ">
                    {otp}
                </span>
            </div>

            <p style="font-size: 15px; color: #555;">
                ⏳ <strong>This OTP is valid for 5 Minutes .</strong><br>
                Please do not share it with anyone.
            </p>

            <p style="font-size: 15px; color: #888; margin-top: 20px;">
                If you did not request this, feel free to ignore this message. No action will be taken.
            </p>

            <br>
            <p style="font-size: 16px;">
                With calm and care,<br>
                <strong style="color: #4a90e2;">The Breathe Team 🌿</strong>
            </p>
        </div>
        """

        text_content = strip_tags(html_content)

        email_message = EmailMultiAlternatives(
            subject="🌟 Your Breathe OTP – Begin Your Calm Journey",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        # Store user info in session temporarily
        request.session["username"] = username
        request.session["email"] = email
        request.session["password"] = password

        messages.success(request, "We've sent a One-Time Password (OTP) to your email. Please verify to continue.")
        return redirect("otp_varify")

    return render(request, "user/register.html")


def otp_varify(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("otp")
        otp_time_str = request.session.get("otp_time")

        if not saved_otp or not otp_time_str:
            messages.error(request, "Session expired or OTP not found. Please request a new OTP.")
            return redirect("register")

        # Parse saved OTP time
        otp_time = datetime.strptime(otp_time_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        # Check OTP expiration: valid for 5 minutes
        if (now - otp_time).total_seconds() > 300:
            messages.error(request, "OTP expired. Please request a new one.")
            return redirect("register")

        # Match OTP
        if entered_otp == saved_otp:
            username = request.session.get("username")
            email = request.session.get("email")
            password = request.session.get("password")

            if not all([username, email, password]):
                messages.error(request, "Session data incomplete. Please register again.")
                return redirect("register")

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Create initial digital coin record
            DigitalCoin.objects.get_or_create(user=user, defaults={"amount": 0})

            # Handle referral reward
            referral_code = request.session.get("referral_code")
            if referral_code:
                try:
                    referrer = ReferralLink.objects.get(code=referral_code).user
                    coin, _ = DigitalCoin.objects.get_or_create(user=referrer)
                    coin.amount += 1
                    coin.save()
                except ReferralLink.DoesNotExist:
                    pass

            # Clear session
            request.session.flush()

            messages.success(request, "OTP verified successfully! You can now log in.")
            return redirect("signin")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "user/otp.html")
from .models import Subscription

from django.views.decorators.csrf import csrf_exempt

from userdata.models import UserAgreement
from django.utils.http import url_has_allowed_host_and_scheme
@csrf_exempt
def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            login(request, user)
            messages.success(request, "You have successfully logged in!")

            # Check agreement
            agreement, _ = UserAgreement.objects.get_or_create(user=user)
            if not agreement.agreed:
                return redirect('liability')
            
            # Handle ?next= redirect
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            # Check subscription
            if Subscription.objects.filter(user=user).exists():
                return redirect('home')
            else:
                # return redirect('subscriptions')
                return redirect('home')

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'user/signin.html')


def user_logout(request):
    logout(request)
    return redirect('signin')  # Redirect the user to the homepage or any other page



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random

def forget_password(request):
    message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)

            send_mail(
                'Your OTP for password reset',
                f'Your OTP is {otp}',
                'noreply@breathewithmeapp.com',  # must match your SMTP login email
                [email],
                fail_silently=False,
            )
            return redirect('verify_otp')
        except User.DoesNotExist:
            message = 'User with this email does not exist.'

    return render(request, 'user/password/forget_password.html', {'message': message})

def verify_otp(request):
    message = ''
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session.get('reset_otp'):
            return redirect('reset_password')
        else:
            message = 'Invalid OTP.'
    return render(request, 'user/password/verify_otp.html', {'message': message})

def reset_password(request):
    message = ''
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.session.get('reset_email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            # Clear session data after password reset
            request.session.pop('reset_email', None)
            request.session.pop('reset_otp', None)
            return redirect('signin')
        except User.DoesNotExist:
            message = 'Something went wrong.'
    return render(request, 'user/password/reset_password.html', {'message': message})

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

from datetime import datetime, timedelta

# Handle free subscriptions with proper date calculation
def free_subscription(request, plan_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    
    try:
        # Get the selected plan from the database
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        # Verify that the plan is actually free
        if plan.price == 0:
            # Set start date to today
            start_date = datetime.now().date()
            
            # Set end date based on plan duration
            end_date = None
            if plan.duration:
                end_date = start_date + timedelta(days=plan.duration)
            
            # Create subscription record in the database
            subscription = Subscription(
                user=request.user,
                plan=plan,
                payment_status='Completed',
                payment_transaction_id='FREE',
                start_date=start_date,
                end_date=end_date
            )
            subscription.save()
            
            # Redirect to home page or a success page
            return redirect('home')  # Redirect to home after successful subscription
        else:
            # If someone tries to get a paid plan for free, redirect to subscriptions
            return redirect('subscriptions')
            
    except SubscriptionPlan.DoesNotExist:
        return redirect('subscriptions')
    
      
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
from django.urls import reverse

# @check_subscription
def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('signin'))  # replace 'signin' with your sign-in URL name

    userdata = Userdata.objects.filter(user=request.user).first()
    username = request.user.username
    return render(request, 'user/home.html', {'username': username, 'userdata': userdata})

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
    return render(request, 'subscription_expired.html', {'username': username,'userdata': userdata})

# //////////////////////////////////// SubscriptionPlan CHECK End ////////////////////////////////////////

@login_required
def user_subscription_page(request):
    user = request.user
    current_subscription = Subscription.objects.filter(user=user).order_by('-subscription_date').first()
    all_plans = SubscriptionPlan.objects.all()

    context = {
        'current_subscription': current_subscription,
        'all_plans': all_plans,
    }
    return render(request, 'user/subscription_page.html', context)


# All settings thing --------------------------------------------------------------------------------------------------------
def user_push_notifications(request):
    return render(request,'user/settings/push_notifications.html')

def user_email_notifications(request):
    return render(request,'user/settings/email_notifications.html')

def user_privacy_settings(request):
    return render(request,'user/settings/user_privacy_settings.html')

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def delete_account(request):
    if request.method == 'POST':
        # Get the password entered by the user
        password = request.POST.get('password')
        
        # Authenticate user with the entered password
        user = authenticate(request, username=request.user.username, password=password)
        
        if user is not None:
            # Password is correct, delete user
            request.user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('home')  # Redirect to home page or login page after deletion
        else:
            messages.error(request, "Incorrect password. Please try again.")
            return redirect('user_privacy_settings')  # Stay on the settings page if password is wrong
    return redirect('user_privacy_settings')  # In case the method is not POST

from testapp.models import TestExercise
from django.db.models.functions import Lower
from testapp.models import TestExercise
from musicapp.models import SavedMusic
from django.db.models.functions import Lower
from django.db.models.functions import Lower, Coalesce
from django.db.models import Value
from django.shortcuts import get_object_or_404
from activityapp.models import TestExerciseActivity

def library_list(request):
    songs = TestExercise.objects.annotate(
        sort_artist=Coalesce(Lower('artist'), Value('zzzz')),
        sort_title=Coalesce(Lower('title'), Value(''))
    ).order_by('sort_artist', 'sort_title')

    saved_song_ids = []
    if request.user.is_authenticated:
        saved_song_ids = SavedMusic.objects.filter(user=request.user).values_list('music_id', flat=True)

        # Track play count for selected song_id if present
        selected_song_id = request.GET.get('song_id')
        if selected_song_id:
            song = get_object_or_404(TestExercise, pk=selected_song_id)
            activity, created = TestExerciseActivity.objects.get_or_create(
                user=request.user,
                exercise=song,
                defaults={'play_count': 1}
            )
            if not created:
                activity.play_count += 1
                activity.save()

    return render(request, 'user/user_playlist.html', {
        'songs': songs,
        'saved_song_ids': saved_song_ids,
    })

from django.contrib.auth.decorators import login_required

@login_required
def liability(request):
    if request.method == 'POST':
        agreement = UserAgreement.objects.get(user=request.user)
        agreement.agreed = True
        agreement.save()
        return redirect('home')
    return render(request, 'user/liability.html')
