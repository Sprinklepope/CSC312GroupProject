from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Flight

class FlightSelectView(ListView):
    model = Flight
    context_object_name = 'flights'
    ordering = ['flightDateTime']

def seatselect(request):
    return render(request, 'booking/seatselect.html')

def infocollect(request):
    return render(request, 'booking/infocollect.html')

def payment(request):
    return render(request, 'booking/payment.html')

def confirmation(request):
    return render(request, 'booking/confirmation.html')
