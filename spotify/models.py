from django.db import models
from api.models import Room, Users, Messages, Google_token
from django.utils import timezone


class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)


class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    song_id = models.CharField(max_length=50)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)


class Queue(models.Model):
    user_id = models.ForeignKey( Users, on_delete=models.CASCADE)
    room_id=models.ForeignKey(Room , on_delete=models.CASCADE)
    added_on=models.DateTimeField(null=True)
    tracks=models.JSONField(default=dict({'tracks':[]}))
    # votes=models.IntegerField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # converting utc to itc , the gap is 5.5 hours
        self.send_on=timezone.now() + timezone.timedelta(hours=5.5)
        #print("timezome.now()::", self.send_on)
        #     self.created = timezone.now()
        # self.modified = timezone.now()
        return super(Queue , self).save(*args, **kwargs)
