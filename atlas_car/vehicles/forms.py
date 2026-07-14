from django import forms
from .models import Vehicle, VehicleOption


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'license_plate', 'brand', 'model', 'year', 'color',
            'category', 'transmission', 'seats', 'mileage',
            'last_revision', 'daily_price', 'deposit', 'photo',
            'status', 'maintenance_threshold'
        ]
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'last_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'daily_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VehicleFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + Vehicle.CATEGORY_CHOICES,
        required=False, widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Vehicle.STATUS_CHOICES,
        required=False, widget=forms.Select(attrs={'class': 'form-control'})
    )
    brand = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'})
    )
    transmission = forms.ChoiceField(
        choices=[('', 'All')] + Vehicle.TRANSMISSION_CHOICES,
        required=False, widget=forms.Select(attrs={'class': 'form-control'})
    )


class VehicleOptionForm(forms.ModelForm):
    class Meta:
        model = VehicleOption
        fields = ['name', 'daily_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'daily_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
