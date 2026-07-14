from django import forms
from .models import Payment, Deposit


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reservation', 'method', 'amount', 'reference']
        widgets = {
            'reservation': forms.Select(attrs={'class': 'form-control'}),
            'method': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['reservation', 'amount_received', 'amount_returned', 'return_date', 'notes']
        widgets = {
            'reservation': forms.Select(attrs={'class': 'form-control'}),
            'amount_received': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'amount_returned': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
