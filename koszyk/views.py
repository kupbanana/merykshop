from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from sklep.models import Produkt
from .koszyk import Koszyk
from .forms import FormularzDodajProduktDoKoszyka


@require_POST
def koszyk_dodaj(request, produkt_id):
    koszyk = Koszyk(request)
    produkt = get_object_or_404(Produkt, id=produkt_id)
    form = FormularzDodajProduktDoKoszyka(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        koszyk.dodaj(produkt=produkt,
                 ilosc=cd['ilosc'],
                 nadpisz_ilosc=cd['nadpisz'])
    return redirect('koszyk:koszyk_szczegoly')


@require_POST
def koszyk_usun(request, produkt_id):
    koszyk = Koszyk(request)
    produkt = get_object_or_404(Produkt, id=produkt_id)
    koszyk.usun(produkt)
    return redirect('koszyk:koszyk_szczegoly')


def koszyk_szczegoly(request):
    koszyk = Koszyk(request)
    for item in koszyk:
        item['uaktualnij_formularz_ilosc'] = FormularzDodajProduktDoKoszyka(initial={'ilosc': item['ilosc'],
                                                                   'nadpisz': True})
    return render(request, 'koszyk/szczegoly.html', {'koszyk': koszyk})
