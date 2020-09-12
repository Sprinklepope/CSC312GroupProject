from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.FlightInfo.as_view(), name='report'),
    path('downloadinfo/', views.downloadinfo, name='downloadinfo'),
]
