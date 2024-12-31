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

def theme2(request):
    return render(request, 'mainapp/theme2.html')

def theme3(request):
    return render(request, 'mainapp/theme3.html')

def theme4(request):
    return render(request, 'mainapp/theme4.html')

def theme5(request):
    return render(request, 'mainapp/theme5.html')



# Starting of Auth here ------------------------------------------------------------------
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Function to generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Register view
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # Generate OTP and send email
        otp = generate_otp()
        request.session['otp'] = otp  # Save OTP in session for verification

        # Send OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Save user data temporarily to session for OTP verification
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('otp_varify')  # Redirect to OTP verification page
    
    return render(request, 'user/register.html')

# OTP verification view
def otp_varify(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        
        # Verify OTP
        if int(entered_otp) == request.session.get('otp'):
            # OTP is correct, create user in the database
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            # Create user in the database
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Clear the session data
            del request.session['otp']
            del request.session['username']
            del request.session['email']
            del request.session['password']

            messages.success(request, "OTP verified successfully! You can now login.")
            return redirect('signin')  # Redirect to login page
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    
    return render(request, 'user/otp.html')

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

def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'user/home.html', {'username': username})

def library(request):
    return render(request, 'user/library.html')

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
def profile(request):
    return render(request, 'user/profile.html')

def language(request):
    return render(request, 'user/language.html')

def sequrity(request):
    return render(request, 'user/sequrity.html')

def user_settings(request):
    return render(request, 'user/settings.html')
# Profile go there End --------------------------------------------------------------------------------




# Custom Features Starts here ------------------------------------------------------------------------

def music_player(request):
    return render(request, 'myapp/music_player.html')