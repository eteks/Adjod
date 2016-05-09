from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from adjod.models import UserProfile
from advertisement.models import *

    
class ChatMessage(models.Model):
    sender   = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    product=models.ForeignKey(Product)
    message  = models.CharField(max_length=200, null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add = True)
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now = True)
    sender_image = models.CharField(max_length=200, null=True, blank=True)
    receiver_image = models.CharField(max_length=200, null=True, blank=True)
    
    def __unicode__(self):
        return self.sender    

class LastActive(models.Model):    
    user   = models.OneToOneField(UserProfile, primary_key = True)
    received_at = models.DateTimeField(auto_now = True)
    session = models.ForeignKey(Session, related_name='session_active')

    def __str__(self):
        return str(self.user.id)

# class VideoSession(models.Model):
#     sender   = models.ForeignKey(User, related_name = 'sender_user1')
#     receiver = models.ForeignKey(User, related_name = 'receiver_user1')
#     session_id  = models.CharField(max_length = 255)
#     token_id    = models.TextField()
    