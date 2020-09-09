from django.urls import path
from . import views

urlpatterns = [
    path('flight/', views.FlightSelectView.as_view(), name='booking-flight'),
    path('seat/', views.seatselect, name='booking-seat'),
    path('info/', views.infocollect, name='booking-info'),
    path('pay/', views.payment, name='booking-pay'),
    path('confirm/', views.confirmation, name='booking-confirm'),
]