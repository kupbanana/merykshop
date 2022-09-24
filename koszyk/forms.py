from django import forms


Wybierz_ILOSCI_PRODUKTOW = [(i, str(i)) for i in range(1, 21)]


class FormularzDodajProduktDoKoszyka(forms.Form):
    ilosc = forms.TypedChoiceField(
                                choices=Wybierz_ILOSCI_PRODUKTOW,
                                coerce=int)
    nadpisz = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
