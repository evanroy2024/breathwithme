from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ReferralLink ,DigitalCoin

from django.contrib.auth.decorators import login_required
from .models import ReferralLink, DigitalCoin
import qrcode
from io import BytesIO
from django.http import HttpResponse


from django.shortcuts import render, get_object_or_404

NGROK_URL = "https://2474-152-58-180-81.ngrok-free.app/"  # Your actual URL

@login_required
def generate_referral_link(request):
    referral, created = ReferralLink.objects.get_or_create(user=request.user)
    # Updated to point to referral-preview
    referral_link = f"{NGROK_URL}referal/referral-preview/?ref={referral.code}"
    
    return render(request, "referal/referral.html", {"referral_link": referral_link})


@login_required
def generate_qr_code(request):
    referral, created = ReferralLink.objects.get_or_create(user=request.user)
    # Updated to point to referral-preview
    referral_link = f"{NGROK_URL}referal/referral-preview/?ref={referral.code}"

    # Create QR Code
    qr = qrcode.make(referral_link)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)
    
    return HttpResponse(buffer.read(), content_type='image/png')


def mycoins(request):
    digital_coins = DigitalCoin.objects.get(user=request.user)
    return render(request, "referal/mycoins.html", {'digital_coins': digital_coins})


# NEW: Intermediate referral preview page
def referral_preview(request):
    ref_code = request.GET.get('ref')
    referral = get_object_or_404(ReferralLink, code=ref_code)
    ref_user = referral.user

    context = {
        'ref_user': ref_user,
        'ref_code': ref_code
    }

    return render(request, "referal/referral_preview.html", context)



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from mainapp.models import Subscription


@login_required
def extend_subscription(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
        digital_coin = DigitalCoin.objects.get(user=request.user)

        if digital_coin.amount >= 25:  # Check if user has enough coins
            digital_coin.amount -= 25  # Deduct 25 coins
            digital_coin.save()

            if subscription.end_date:
                subscription.end_date += timedelta(days=365)
            else:
                subscription.start_date = now().date()
                subscription.end_date = subscription.start_date + timedelta(days=365)

            subscription.save()
            return JsonResponse({"message": "Subscription extended successfully!", "new_end_date": subscription.end_date, "remaining_coins": digital_coin.amount})
        else:
            return JsonResponse({"error": "Not enough coins"}, status=400)

    except Subscription.DoesNotExist:
        return JsonResponse({"error": "Subscription not found"}, status=404)
    except DigitalCoin.DoesNotExist:
        return JsonResponse({"error": "Digital coin balance not found"}, status=404)