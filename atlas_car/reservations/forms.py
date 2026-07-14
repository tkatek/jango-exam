from django import forms
from .models import Reservation, ReservationOption


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'customer', 'vehicle', 'pickup_date', 'return_date',
            'pickup_location', 'return_location'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_location': forms.Select(attrs={'class': 'form-control'}),
            'return_location': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from vehicles.models import Vehicle
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='available')


class ReservationOptionForm(forms.ModelForm):
    class Meta:
        model = ReservationOption
        fields = ['option', 'quantity']
        widgets = {
            'option': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


ReservationOptionFormSet = forms.inlineformset_factory(
    Reservation, ReservationOption,
    form=ReservationOptionForm, extra=1, can_delete=True
)
