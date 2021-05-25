from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
  path('event_admin/<int:event_id>/', views.event_admin, name='event_admin'),
  path('create_event/', views.create_event, name='create_event'),
  path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
  path('event_enroll/<int:event_id>/', views.event_enroll, name='event_enroll'),
  path('event_unenroll/<int:event_id>/', views.event_unenroll, name='event_unenroll'),
  path('create_notification/<int:event_id>/', views.create_notification, name='create_notification'),
  path('view_notification/<int:notif_id>/', views.view_notification, name='view_notification'),
]