from django import forms

class PayementForm(forms.Form):
    name = forms.CharField(label='Name on Card', max_length=100)
    cardNo = forms.CharField(label='Card Number', max_length=16)
    cvv = forms.CharField(label='CVV', max_length=4)