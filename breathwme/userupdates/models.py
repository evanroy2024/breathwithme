from django.db import models

class Notifications(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='notifications_images/', blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled Notification"


from django.db import models
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model

User = get_user_model()

# Import your preference model
from userdata.models import UserSettingsPreference  # Adjust import if it's in another app
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.core.files.storage import default_storage
from django.conf import settings
from django.conf import settings
from email.mime.image import MIMEImage
import os 

User = get_user_model()

class EmailNotification(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='email_notifications/', null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email: {self.subject} at {self.sent_at}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        recipients = User.objects.filter(
            userpreferancedata__email_notification=True
        ).values_list('email', flat=True).exclude(email='')

        for email in recipients:
            msg = EmailMultiAlternatives(
                subject=self.subject,
                body=self.message,
                to=[email]
            )

            # Start building HTML content
            html_content = f"<p>{self.message.replace(chr(10), '<br>')}</p>"

            if self.image:
                image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
                image_cid = 'footerimage'
                html_content += f'<br><img src="cid:{image_cid}" alt="Footer Image" style="max-width:100%; border-radius:8px; margin-top:20px;" />'

                # Attach image as inline content
                with open(image_path, 'rb') as img:
                    mime_img = MIMEImage(img.read())
                    mime_img.add_header('Content-ID', f'<{image_cid}>')
                    mime_img.add_header('Content-Disposition', 'inline', filename=self.image.name)
                    msg.attach(mime_img)

            msg.attach_alternative(html_content, "text/html")
            msg.send()



from django.db import models
from django.contrib.auth.models import User

class PushNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="push_notifications", null=True, blank=True)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.token}"


from django.db import models

class PushNotificationMessage(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - Sent: {self.sent}"



# For testing Firebase FCM --------------------------------------------------------------------------------- 
from django.db import models

class DeviceToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.URLField(blank=True, null=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title