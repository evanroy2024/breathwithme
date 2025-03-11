from django.shortcuts import redirect
from django.utils.timezone import now
from .models import Subscription

def check_subscription(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                subscription = Subscription.objects.get(user=request.user)
                if subscription.end_date and subscription.end_date < now().date():
                    return redirect('subscription_expired')  # Redirect if expired
            except Subscription.DoesNotExist:
                return redirect('subscription_expired')  # Redirect if no subscription

        return view_func(request, *args, **kwargs)

    return wrapper
