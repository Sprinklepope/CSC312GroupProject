from django.shortcuts import render, reverse
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from booking.models import Ticket_History
from django.http import HttpResponseRedirect
from datetime import datetime

class TicketSelectView(LoginRequiredMixin, ListView):
    '''
    Displays all orders associated with current user.
    Extends ListView Default View
    '''
    model = Ticket_History
    context_object_name = 'tickets'
    template_name = 'cancellation/ticket_history_list.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        context['tickets'] = Ticket_History.objects.filter(booked_MemberID=self.request.user, flightNo__flightDateTime__gte=datetime.now(), ticket_Cancelled=False)
        context['orders'] = list(set(context['tickets'].values_list('bookingRef')))
        return context

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    Changes ticket cancelation flag to true for selected ticket
    Extends DeleteView Default View
    '''
    model = Ticket_History
    template_name = 'cancellation/ticket_history_delete.html'
    context_object_name = 'ticket'

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.ticket_Cancelled = True
        ticket.save()
        flight = ticket.flightNo
        flight.seatsAvailable = flight.seatsAvailable + 1
        flight.save()
        return HttpResponseRedirect(reverse('cancellation-list'))

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.booked_MemberID:
            return True
        return False