from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Plane(models.Model):
    planeID = models.CharField(max_length=5, primary_key=True, unique=True)
    planeType = models.CharField(max_length=10)
    seatsAvailable = models.IntegerField()
    seatsPerRow = models.IntegerField()
    seatsEconomyClass = models.IntegerField()
    seatsBusinessClass = models.IntegerField()
    seatsFirstClass = models.IntegerField()


class Flight(models.Model):
    flightNo = models.CharField(max_length=5)
    airline = models.CharField(max_length=100)
    seatsAvailable = models.IntegerField()
    departureLocation = models.CharField(max_length=100)
    arrivalLocation = models.CharField(max_length=100)
    flightDateTime = models.DateTimeField()
    flightDuration = models.CharField(max_length=20)
    departureTerminal = models.CharField(max_length=3)
    planeID = models.ForeignKey(Plane, on_delete=models.CASCADE)
    economyCost = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    businessCost = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    firstCost = models.DecimalField(default=0, decimal_places=2, max_digits=12)

class Ticket_History(models.Model):
    ECONOMY = 'e'
    BUSINESS = 'b'
    FIRST = 'f'
    CLASS_CHOICES = [
        (ECONOMY, 'Economy Class'),
        (BUSINESS, 'Business Class'),
        (FIRST, 'First Class')
    ]

    bookingRef = models.CharField(max_length=6)
    seatNo = models.CharField(max_length=3)
    passenger_passportNo = models.CharField('Passanger ID/Passport Number', max_length=13)
    booked_MemberID = models.ForeignKey(User, on_delete=models.CASCADE)
    passengerNames = models.CharField('Passanger Name', max_length=100)
    passengerSurname = models.CharField('Passanger Surname',max_length=100)
    flightNo = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seatClass = models.CharField(max_length=1, choices=CLASS_CHOICES, default=ECONOMY)
    ticket_Cancelled = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)