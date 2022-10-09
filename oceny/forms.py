from django.forms import Form
from django import forms
from .models import Ocena


class FormularzDodajOcene(forms.Form):
    gwiazdki=forms.IntegerField(min_value=1,max_value=5)

