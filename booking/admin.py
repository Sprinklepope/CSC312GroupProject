from django.contrib import admin
from .models import Planes, Flights, Ticket_History

admin.site.register(Planes)
admin.site.register(Flights)
admin.site.register(Ticket_History)
