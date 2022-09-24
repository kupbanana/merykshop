from django.shortcuts import render, get_object_or_404
from koszyk.forms import FormularzDodajProduktDoKoszyka
from .models import Kategoria, Produkt


def lista_produktow(request, kategoria_skrot_url=None):
    kategoria = None
    kategorie = Kategoria.objects.all()
    produkty = Produkt.objects.filter(dostepny=True)
    if kategoria_skrot_url:
        kategoria = get_object_or_404(Kategoria, skrot_url=kategoria_skrot_url)
        produkty = produkty.filter(kategoria=kategoria)
    return render(request,
                  'sklep/produkt/lista.html',
                  {'kategoria': kategoria,
                   'kategorie': kategorie,
                   'produkty': produkty})

def znajdz_produkty(request):
    kategoria=None
    szukana_nazwa=None
    kategorie = Kategoria.objects.all()
    produkty = Produkt.objects.all()
    if request.method=="POST":
        szukana_nazwa = request.POST['szuknazwa']
        produkty = Produkt.objects.filter(nazwa__contains=szukana_nazwa)
    return render(request,
                  'sklep/produkt/lista.html',
                  {'szukane': szukana_nazwa,
                   'kategoria': kategoria,
                   'kategorie': kategorie,
                   'produkty': produkty})


def szczegoly_produktu(request, id, skrot_url, kategoria_skrot_url=None):
    kategoria=None
    kategorie = Kategoria.objects.all()
    produkt = get_object_or_404(Produkt,
                                id=id,
                                skrot_url=skrot_url,
                                dostepny=True)
    formularz_dodaj_do_koszyka = FormularzDodajProduktDoKoszyka()

    if kategoria_skrot_url:
        kategoria = get_object_or_404(Kategoria, skrot_url=kategoria_skrot_url)

    return render(request,
                  'sklep/produkt/szczegoly.html',
                  {'kategoria': kategoria,
                   'kategorie': kategorie, 
                   'produkt': produkt,
                   'formularz_dodaj_do_koszyka': formularz_dodaj_do_koszyka})
