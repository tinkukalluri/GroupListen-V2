from django.db import models
from django.utils import timezone

# Create your models here.

# model is just a table 

import string
import random


def generate_unique_code():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code

class Users(models.Model):
    google_uid=models.CharField(max_length=255 , null=True , unique=True)
    email_uid=models.CharField(max_length=255 , null=True)
    username=models.CharField(max_length=255 , null=True )
    password=models.CharField(max_length=255 , null=True)
    photoURL=models.CharField(max_length=1000 , null=True)
    

class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.ForeignKey(Users ,on_delete=models.CASCADE )
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    current_song=models.CharField(max_length=50 , null=True)
    guests=models.JSONField(default={
        'guests':[]
    })
    class meta:
        verbose_name = "rooms"
        verbose_name_plural = "all rooms"

class Messages(models.Model):
    msg_from=models.ForeignKey(Users , on_delete=models.CASCADE )
    room_id=models.ForeignKey(Room , on_delete=models.CASCADE)
    text=models.TextField()
    delivered=models.BooleanField(default=False)
    seen=models.BooleanField(default=False)
    send_on=models.DateTimeField()
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # converting utc to itc , the gap is 5.5 hours
        self.send_on=timezone.now() + timezone.timedelta(hours=5.5)
        #print("timezome.now()::", self.send_on)
        #     self.created = timezone.now()
        # self.modified = timezone.now()
        return super(Messages , self).save(*args, **kwargs)


class Google_token(models.Model):
    u_id=models.ForeignKey(Users , on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)


