from django.urls import path
from . import views

urlpatterns = [
    path('ticketlist/', views.TicketSelectView.as_view(), name='cancellation-list'),
    path('cancel/<pk>', views.TicketDeleteView.as_view(), name='cancellation-cancel'),
]