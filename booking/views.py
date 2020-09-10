from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import reverse
from .models import Flight, Ticket_History

class FlightSelectView(ListView):
    model = Flight
    context_object_name = 'flights'
    ordering = ['flightDateTime']

@login_required
def seatselect(request, flight):
    if request.method == "POST":
        if len(request.POST) > 1:
            return redirect('booking-info')

    flightInfo = Flight.objects.get(flightNo=flight)
    flightHistory = Ticket_History.objects.filter(flightNo=flightInfo, ticket_Cancelled=False)
    col = int(flightInfo.planeID.seatsPerRow)
    row = int(flightInfo.planeID.seatsAvailable / col)
    mid = (col//2)
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    taken_seats = [(int(ticket.seatNo[1:]), letters.index(ticket.seatNo[0])) for ticket in flightHistory]
    firstMark = (flightInfo.planeID.seatsFirstClass)/col
    busMark = (flightInfo.planeID.seatsBusinessClass/col)+firstMark
    rows = range(1, row+1)
    cols = range(col)
    seats = []
    for r in rows:
        seats.append([])
        for c in cols:
            seats[r-1].append((r,c))
    context = {
        'flightInfo': flightInfo,
        'seats': seats,
        'col': col,
        'firstMark': firstMark,
        'busMark': busMark,
        'mid': mid,
        'letters': list(letters[:col//2])+['Isle']+list(letters[col//2:col]),
        'takenSeats': taken_seats
    }
    return render(request, "booking/seatselect.html", context)

@login_required
def infocollect(request):
    return render(request, 'booking/infocollect.html')

@login_required
def payment(request):
    return render(request, 'booking/payment.html')

@login_required
def confirmation(request):
    return render(request, 'booking/confirmation.html')
