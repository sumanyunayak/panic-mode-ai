from django.urls import path
from . import views

urlpatterns = [
    path('triage/', views.triage, name='triage'),
    path('checkin/', views.checkin, name='checkin'),
    path('explode/', views.explode, name='explode'),
    path('recovery/', views.recovery, name='recovery'),
]