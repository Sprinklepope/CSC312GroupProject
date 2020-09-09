from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Flights(models.Model):
    flightNo = models.CharField(max_length=5, primary_key=True, unique=True)
    airline = models.CharField(max_length=100)
    seatsAvailable = models.IntegerField()
    departureLocation = models.CharField(max_length=100)
    arrivalLocation = models.CharField(max_length=100)
    flightDateTime = models.DateTimeField()
    flightDuration = models.DecimalField()
    departureTerminal = models.CharField(max_length=3)
    planeID = models.ForeignKey(Planes)

class Ticket_History(models.Model):
    bookingRef = models.CharField(max_length=6)
    seatNo = models.CharField(max_length=3)
    passenger_passportNo = models.CharField(max_length=13)
    booked_MemberID = models.ForeignKey(User, on_delete=models.CASCADE)
    passengerNames = models.CharField(max_length=100)
    passengerSurname = models.CharField(max_length=100)
    flightNo = models.ForeignKey(Flights)
    ticket_Cancelled = models.BooleanField(default=False)

class Planes(models.Model):
    planeID = models.CharField(max_length=5, primary_key=True, unique=True)
    planeType = models.CharField(max_length=10)
    seatsAvailable = models.IntegerField()
    seatsPerRow = models.IntegerField()
    seatCollumns = models.IntegerField()
    seatsEconomyClass = models.IntegerField()
    seatsBusinessClass = models.IntegerField()
    seatsFirstClass = models.IntegerField()
    economyCost = models.DecimalField()
    businessCost = models.DecimalField()
    firstCost = models.DecimalField()