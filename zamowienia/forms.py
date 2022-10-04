from django import forms
from .models import Zamowienie
from uzytkownicy.models import UzytkownikProfil


class OrderCreateForm(forms.Form):
    imie = forms.CharField(max_length=50)
    nazwisko = forms.CharField(max_length=50)
    email = forms.EmailField()
    adres = forms.CharField(max_length=250)
    kod_pocztowy = forms.CharField(max_length=20)
    miasto = forms.CharField(max_length=100)
       