from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from booking.models import Flight, Ticket_History, Plane
from django.views.generic import ListView
import csv


# Create your views here.
class FlightInfo(ListView):
    template_name = 'management/management_list.html'
    model = Flight
    context_object_name = 'flights'
    ordering = ['flightDateTime']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = []
        for flight in Flight.objects.all():
            numseats = flight.planeID.seatsAvailable
            a.append(numseats-flight.seatsAvailable)
        context['flightsize'] = a
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = []
        c = []
        for flight in Flight.objects.all():
            numseats = flight.planeID.seatsAvailable
            c.append(numseats)
            a.append(numseats - flight.seatsAvailable)
        b = Flight.objects.all()
        context['triinfo'] = zip(a,b,c)
        return context


def downloadinfo(request):
    # Create the HttpResponse object with the appropriate CSV header.
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="current.csv"'
        writer = csv.writer(response)
        writer.writerow(['Flight', 'Airline', 'Date', 'Total Seats', 'Available Seats', 'Taken Seats'])
        for flight in Flight.objects.all():
            numseats = flight.planeID.seatsAvailable
            writer.writerow([flight.flightNo, flight.airline, flight.flightDateTime, numseats, flight.seatsAvailable, numseats-flight.seatsAvailable])
    else:
        response = HttpResponse("<html><body>You do not have the required credentials to access this page</body></html>")
    return response




