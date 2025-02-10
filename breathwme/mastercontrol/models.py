from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    passcode = models.CharField(max_length=6, blank=True, null=True)  # Secret code to join the room
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_chatrooms')  # Admin of the room
    
    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in {self.chatroom.name}"
