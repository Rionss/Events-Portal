from django.shortcuts import render, redirect

from users.models import User
from .models import event, event_notification

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

from .forms import EventCreationForm, EventUpdateForm, EventRegistrationForm, NotificationForm, ViewNotificationForm

# Create your views here.
def index(request):
  if request.user.is_authenticated:
    enrolled_events = event.objects.filter(participants=request.user)
    if enrolled_events:
      for current_event in enrolled_events:
        try:
          notifications = event_notification.objects.filter(event=current_event).exclude(viewers=request.user)
          context = {
            'enrolled_events': enrolled_events,
            'events': event.objects.all(),
            'notifications': notifications
          }
        except ObjectDoesNotExist():
          context = {
            'enrolled_events': enrolled_events,
            'events': event.objects.all(),
          }
    else:
      context = {
        'enrolled_events': enrolled_events,
        'events': event.objects.all(),
      }
    enrolled_events = event.objects.filter(participants=request.user)
    return render(request, 'core/index.html', context)
  else:
    return render(request, 'core/index.html', {
      'events': event.objects.all(),
    })

@login_required
def view_notification(request, notif_id):
  event_id = event_notification.objects.get(id=notif_id).event.id
  instance = event_notification.objects.get(id=notif_id)
  form = ViewNotificationForm(instance=instance)
  if request.method == 'POST':
    form = ViewNotificationForm(request.POST, instance=instance)
    if form.is_valid():
      post=form.save(commit=False)
      post.viewers.add(request.user)
      post.save()
      return redirect('event_detail', event_id)

@login_required
def event_detail(request, event_id):
  try:
    event.objects.get(id=event_id, participants=request.user)
    current_event = event.objects.get(id=event_id)
    return render(request, 'core/event_detail.html', {
      'event': event.objects.get(id=event_id),
      'enrolled': True,
      'notifications': event_notification.objects.filter(event=current_event),
    })
  except ObjectDoesNotExist:
    return render(request, 'core/event_detail.html', {
      'event': event.objects.get(id=event_id),
      'enrolled': False,
    })

@login_required
def create_event(request):
  form = EventCreationForm()
  if request.method == 'POST':
    form = EventCreationForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.event_host = request.user
      post.date = request.POST['date']
      post.time = request.POST['time']
      post.save()
      return redirect('profile')
    else:
      return render(request, 'core/create_event.html', {
        'form': form,
        'error': True,
      })
  return render(request, 'core/create_event.html', {
    'form': form,
  })

@login_required
def edit_event(request, event_id):
  if event.objects.get(id=event_id).event_host == request.user:
    instance = event.objects.get(id=event_id, event_host=request.user)
    if instance:
      form = EventUpdateForm(instance=instance)
      if request.method == 'POST':
          form = EventUpdateForm(request.POST, request.FILES, instance=instance)
          if form.is_valid():
            form.save()
            return redirect('index')
          else:
            return render(request, 'event_edit.html', {
              'form': form,
              'event': event.objects.get(id=event_id),
              'error': True,
            })
      return render(request, 'core/edit_event.html', {
        'form': form,
        'event': event.objects.get(id=event_id),
      })
  else:
    return redirect('index')
  return render(request, 'core/edit_event.htm', {
    'form': form,
  })

@login_required
def event_admin(request, event_id):
  try:
    event.objects.get(id=event_id, event_host=request.user)
    current_event = event.objects.get(id=event_id)
    return render(request, 'core/event_admin.html', {
      'event': event.objects.get(id=event_id),
      'notifications': event_notification.objects.filter(event=current_event),
    })
  except ObjectDoesNotExist:
    return redirect('index')

@login_required
def create_notification(request, event_id):
  if event.objects.get(id=event_id).event_host == request.user:
    form = NotificationForm()
    if request.method == 'POST':
      form = NotificationForm(request.POST)
      if form.is_valid():
        post = form.save(commit=False)
        post.event = event.objects.get(id=event_id)
        post.save()
        return redirect('event_admin', event_id)
      else:
        return render(request, 'core/create_notification.html', {
          'form': form,
          'error': True
        })
    return render(request, 'core/create_notification.html', {
      'form': form,
    })
  else:
    return redirect('index')

@login_required
def event_enroll(request, event_id):
  current_event = event.objects.get(id=event_id)
  if current_event.max_participants >= current_event.participants.count():
    try:
      current_event = event.objects.get(id=event_id, participants=request.user)
      return redirect('index')
    except ObjectDoesNotExist:
      instance = event.objects.get(id=event_id)
      form = EventRegistrationForm(instance=instance)
      if request.method == 'POST':
        form = EventRegistrationForm(request.POST, instance=instance)
        if form.is_valid():
          post = form.save(commit=False)
          post.participants.add(request.user)
          post.save()
          return redirect('event_detail', event_id)  
        else:
          return render(request, 'core/event_registration.html', {
              'form': form,
              'error': True,
            })
      return render(request, 'core/event_registration.html', {
        'form': form,
        'enrolled': False,
      })
  else:
    return redirect('event_detail', event_id)

@login_required
def event_unenroll(request, event_id):
  current_event = event.objects.get(id=event_id)
  if current_event.max_participants >= current_event.participants.count():
    try:
      instance = event.objects.get(id=event_id)
      form = EventRegistrationForm(instance=instance)
      if request.method == 'POST':
        form = EventRegistrationForm(request.POST, instance=instance)
        if form.is_valid():
          post = form.save(commit=False)
          post.participants.remove(request.user)
          post.save()
          return redirect('event_detail', event_id)  
        else:
          return render(request, 'core/event_registration.html', {
              'form': form,
              'error': True,
            })
      return render(request, 'core/event_registration.html', {
        'form': form,
        'enrolled': True,
      })
    except ObjectDoesNotExist:
      current_event = event.objects.get(id=event_id, participants=request.user)
      return redirect('event_detail', event_id)
  else:
    return redirect('event_detail', event_id)