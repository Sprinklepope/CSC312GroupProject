from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.FlightInfo.as_view(), name='management'),
    path('downloadinfo/', views.downloadinfo, name='downloadinfo'),
]
