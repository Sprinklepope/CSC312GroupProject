from django.shortcuts import render

def flightselect(request):
    return render(request, 'booking/flightselect.html')

def seatselect(request):
    return render(request, 'booking/seatselect.html')

def infocollect(request):
    return render(request, 'booking/infocollect.html')

def payment(request):
    return render(request, 'booking/payment.html')

def confirmation(request):
    return render(request, 'booking/confirmation.html')
