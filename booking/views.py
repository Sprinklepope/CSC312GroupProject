from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import reverse
from .models import Flight

class FlightSelectView(ListView):
    model = Flight
    context_object_name = 'flights'
    ordering = ['flightDateTime']

@login_required
def seatselect(request, flight):
    if request.method == "POST":

        if form.is_valid():
            return redirect("/")
    else:
        flightInfo = Flight.objects.get(flightNo=flight)
        col = int(flightInfo.planeID.seatsPerRow)
        row = int(flightInfo.planeID.seatsAvailable / col)
        mid = (col//2)
    context = {
        'flightInfo': flightInfo,
        'row': range(row),
        'col': range(col+1),
        'mid': mid
    }
    return render(request, "booking/seatselect.html", context)

def infocollect(request):
    return render(request, 'booking/infocollect.html')

def payment(request):
    return render(request, 'booking/payment.html')

def confirmation(request):
    return render(request, 'booking/confirmation.html')
