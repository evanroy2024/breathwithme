from django.db import models
from django.contrib.auth.models import User
import uuid

class ReferralLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals")
    code = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:10]  # Generate a unique referral code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

class DigitalCoin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="digital_coins")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.amount} Coins"
