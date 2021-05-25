from django import forms
from .models import event, event_notification

class EventCreationForm(forms.ModelForm):
  class Meta:
    model = event
    fields = ['event_title', 'event_description', 'banner', 'max_participants', 'location']

class EventUpdateForm(forms.ModelForm):
  class Meta:
    model = event
    fields = ['event_title', 'event_description', 'banner', 'max_participants', 'location', 'participants']

class EventRegistrationForm(forms.ModelForm):
  class Meta:
    model = event
    fields = []

class NotificationForm(forms.ModelForm):
  class Meta:
    model = event_notification
    fields = ['notification_title', 'notification_description']

class ViewNotificationForm(forms.ModelForm):
  class Meta:
    model = event_notification
    fields = []