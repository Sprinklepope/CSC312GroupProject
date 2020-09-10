from django.urls import path
from . import views

urlpatterns = [
    path('flight/', views.FlightSelectView.as_view(), name='booking-flight'),
    path('<flight>/seat/', views.seatselect, name='booking-seat'),
    path('<pk>/info/', views.InfoCollectView.as_view(), name='booking-info'),
    path('<booking>/pay/', views.payment, name='booking-pay'),
    path('<booking>/confirm/', views.confirmation, name='booking-confirm'),
]