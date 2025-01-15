from django.shortcuts import render , get_object_or_404
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    # Get the course with its materials
    course = get_object_or_404(Course, id=course_id)
    materials = course.materials.all().order_by('order')
    return render(request, 'courses/course_detail.html', {'course': course, 'materials': materials})

from .models import Item
def Video(request):
    items = Item.objects.all()
    return render(request, 'courses/video.html', {'items': items})