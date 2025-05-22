# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
from .models import PageVisit
import json
from django.utils.timezone import now
import re



@csrf_exempt
def track_activity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            duration = data.get('duration')
            user = request.user if request.user.is_authenticated else None
            today = now().date()

            # Normalize URL by removing trailing numeric segment if present
            # Example: /breathxapp/play/7/ -> /breathxapp/play
            # It removes last "/<number>/" or "/<number>"
            normalized_url = re.sub(r'/\d+/?$', '', url)

            # Now get or create PageVisit with normalized_url
            page_visit, created = PageVisit.objects.get_or_create(
                user=user,
                url=normalized_url,
                date=today,
                defaults={'duration_seconds': 0}
            )

            # Add new duration
            page_visit.duration_seconds += duration
            page_visit.save()

            return JsonResponse({
                'status': 'success',
                'added_seconds': duration,
                'total_seconds': page_visit.duration_seconds,
                'normalized_url': normalized_url,
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid request'}, status=405)