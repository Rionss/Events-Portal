from django.shortcuts import render, redirect

from core.models import event
from users.models import User
from .forms import CreateUserForm, EditProfileForm

from django.contrib.auth.decorators import login_required

from django.utils import timezone

def signup(request):
  if request.method == 'POST':
    form = CreateUserForm(request.POST, request.FILES)
    form.start_date = timezone.now()
    if form.is_valid():
      form.save()
      return redirect('login')
    else:
      return render(request, 'registration/signup.html',{
        'form': form,
        'error': True,
      })
  else:
    form = CreateUserForm()
    return render(request, 'registration/signup.html',{
      'form': form
    })

@login_required
def profile(request):
    return render(request, 'core/dashboard.html', {
      'enrolled_events': event.objects.filter(participants=request.user),
      'hosted_events': event.objects.filter(event_host=request.user)
    })

@login_required
def edit_profile(request):
  user_id = request.user.id
  instance = User.objects.get(id=user_id)
  form = EditProfileForm(instance=instance)
  if request.method == 'POST':
    form = EditProfileForm(request.POST, request.FILES, instance=instance)
    if form.is_valid:
      form.save()
      return redirect('profile')
    else:
      return render(request, 'edit_profile.html', {
        'form': form,
        'error': True,
      })
  return render(request, 'edit_profile.html', {
    'form': form
  })