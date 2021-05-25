from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.
class event(models.Model):
  event_title = models.CharField(max_length=500)
  event_description = models.TextField()
  event_host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_host')
  date = models.DateField()
  time = models.TimeField()
  max_participants = models.IntegerField()
  banner = models.ImageField(upload_to='events/img/banner')
  location = models.CharField(max_length=150)
  participants = models.ManyToManyField(User, related_name='participants')
  def __str__(self):
    return self.event_title

class event_notification(models.Model):
  event = models.ForeignKey(event, on_delete=models.CASCADE, related_name='event')
  notification_title = models.CharField(max_length=200)
  notification_description = models.TextField()
  notification_datetime = models.DateTimeField(default=timezone.now)
  viewers = models.ManyToManyField(User, blank=True)
  
  def __str__(self):
      return f'{self.event}: {self.notification_title}'
  