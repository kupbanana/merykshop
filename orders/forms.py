from django import forms
from .models import Zamowienie


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = ['imie', 'nazwisko', 'email', 'adres',
                  'kod_pocztowy', 'miasto']
