from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Flight, Ticket_History
from .forms import PayementForm
import random
from django.contrib import messages
from datetime import datetime

class FlightSelectView(ListView):
    '''
    Displays all available flights.
    Extends ListView Default View
    '''
    model = Flight
    context_object_name = 'flights'
    ordering = 'flightDateTime'

    def get_queryset(self):
        qs = self.model.objects.filter(flightDateTime__gt=datetime.now()).order_by(self.ordering)
        return qs

@login_required
def seatselect(request, flight):
    '''
    Renders seat selection template.
    On Post Request it determines the selected seats
    and calls InfoCollectView.
    This places relevant ticket info into request.session
    '''
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Checks if request is POST
    if request.method == "POST":
        if len(request.POST) > 1:
            args = request.POST.keys()
            booking = str(random.randint(100000, 999999))   # Generating Booking Number
            seats = []
            # Determining number of types of seats
            classesNo = {
                'e':0,
                'b': 0,
                'f': 0,
            }
            for val in args:
                if val != "csrfmiddlewaretoken":
                    seats.append(((letters[int(val[-2])] + str(val[2:-4])), val[0]))
                    classesNo[val[0]] +=1
            ids=[]
            # Creating initial entry for seats selected
            for seat in seats:
                ticket = Ticket_History(bookingRef=booking, seatNo=seat[0], flightNo=Flight.objects.get(flightNo=flight), booked_MemberID=request.user, seatClass=seat[1])
                ticket.save()
                ids.append(ticket.id)
            # Loading data into session for next views
            request.session['ids'] = ids
            request.session['NoOfSeats'] = len(ids)
            request.session['order'] = booking
            request.session['classes'] = classesNo
            return redirect('booking-info', pk=ids[0])
        else:
            messages.error = (request, 'Please make a selection before submitting')
    # Removing incomplete ticket entries
    Ticket_History.objects.filter(passenger_passportNo__exact='',passengerNames__exact='',passengerSurname__exact='').delete()
    Ticket_History.objects.filter(paid=False).delete()
    # Collecting Context Data to be sent to view
    request.session['flight'] = flight
    flightInfo = Flight.objects.get(flightNo=flight)
    flightHistory = Ticket_History.objects.filter(flightNo=flightInfo, ticket_Cancelled=False)
    taken_seats = [(int(ticket.seatNo[1:]), letters.index(ticket.seatNo[0])) for ticket in flightHistory]
    col = int(flightInfo.planeID.seatsPerRow)
    row = int(flightInfo.planeID.seatsAvailable / col)
    mid = (col//2)
    
    firstMark = (flightInfo.planeID.seatsFirstClass)/col
    busMark = (flightInfo.planeID.seatsBusinessClass/col)+firstMark
    rows = range(1, row+1)
    cols = range(col)
    seats = []

    for r in rows:
        seats.append([])
        for c in cols:
            seats[r-1].append((r,c))

    # Context Data
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

class InfoCollectView(LoginRequiredMixin, UpdateView):
    '''
    Presents form for outstanding ticket information to user
    Extends UpdateView Default View
    '''
    template_name = 'booking/infocollect.html'
    model = Ticket_History
    fields = ['passenger_passportNo','passengerNames', 'passengerSurname']
    context_object_name = 'context'

    # Checking validity of returned form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Determines success url based on whether more seat forms need to be filled or not
    def get_success_url(self):
        if len(self.request.session['ids']) > 1:
            self.request.session['ids'] = self.request.session['ids'][1:]
            return reverse('booking-info',kwargs={'pk': self.request.session['ids'][0]})
        else:
            return reverse('booking-pay', kwargs={'booking': self.request.session['order']})


@login_required
def payment(request, booking):
    '''
    Shows payment breakdown of order.
    Provides a form for bank details.
    '''
    # Checks if request is POST
    if request.method == 'POST':
        form = PayementForm(request.POST)
        # Redirects to confirmation page if form is valid
        if form.is_valid():
            # Decrementing number of available seats for flight
            flight = Flight.objects.get(flightNo=request.session['flight'])
            flight.seatsAvailable = flight.seatsAvailable - request.session['NoOfSeats']
            flight.save()
            return HttpResponseRedirect(reverse('booking-confirm' ,kwargs={'booking': request.session['order']}))
    else:
        form = PayementForm()
    # Collecting Context Data
    orders = Ticket_History.objects.filter(bookingRef=booking)
    flight = Flight.objects.get(flightNo=request.session['flight'])
    classes = request.session['classes']
    prices = {
        'eprice': classes['e']*flight.economyCost,
        'bprice': classes['b']*flight.businessCost,
        'fprice': classes['f']*flight.firstCost,
        'total': classes['e']*flight.economyCost + classes['b']*flight.businessCost + classes['f']*flight.firstCost
    }
    context = {
        'form': form,
        'orders': orders,
        'classes': classes,
        'prices': prices,
        'flight': flight
    }
    # Rendering payment page
    return render(request, 'booking/payment.html', context)

@login_required
def confirmation(request, booking):
    '''
    Displays order confirmation page
    '''
    # Collecting Context Information
    tickets = Ticket_History.objects.filter(bookingRef=booking)
    for ticket in tickets:
        ticket.paid=True
        ticket.save()
    if request.user == tickets[0].booked_MemberID:
        flight = Flight.objects.get(flightNo=request.session['flight'])
        classes = request.session['classes']
        total = classes['e']*flight.economyCost + classes['b']*flight.businessCost + classes['f']*flight.firstCost
        context = {
            'tickets': tickets,
            'total': total,
            'flight': flight,
            'order': request.session['order']
        }
        # Rendering Confirmation Page
        return render(request, 'booking/confirmation.html', context)
    else:
        return HttpResponseForbidden()
