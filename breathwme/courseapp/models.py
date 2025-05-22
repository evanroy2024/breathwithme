from django.db import models
from datetime import date
from embed_video.fields import EmbedVideoField


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', blank=True, null=True , )
    start_date = models.DateField(default=date.today)  # Default start date is today
    end_date = models.DateField(default=date.today)  # Default end date is today
    duration = models.CharField(max_length=50, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Material(models.Model):
    COURSE_MATERIAL_CHOICES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('text', 'Classic Text'),
    ]

    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    material_type = models.CharField(
        max_length=50,
        choices=COURSE_MATERIAL_CHOICES,
        default='video'
    )
    content_url = EmbedVideoField(blank=True, null=True)   # For video/audio URL
    pdf_file = models.FileField(upload_to='materials/pdfs/', blank=True, null=True)  # For classic text PDFs
    order = models.IntegerField(help_text="Material order within the course")

    def __str__(self):
        return f"{self.get_material_type_display()} - {self.course.title}"


from django.db import models

class Item(models.Model):
    video = EmbedVideoField()  # same like models.URLField()



# QUIZES      --------------------------------------------------
from django.db import models
from django.core.exceptions import ValidationError

class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    
    quiz_file = models.FileField(upload_to='quiz_data/', blank=True, null=True)

    def __str__(self):
        return self.title

    def clean(self):
        """Custom clean method to validate CSV format"""
        if self.quiz_file:
            try:
                # Check if the uploaded file is a CSV file
                if not self.quiz_file.name.endswith('.csv'):
                    raise ValidationError("Only CSV files are allowed.")
            except Exception as e:
                raise ValidationError(f"Error reading CSV file: {str(e)}")
