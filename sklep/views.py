from django.shortcuts import render, get_object_or_404, redirect
from koszyk.forms import FormularzDodajProduktDoKoszyka
from django.contrib.auth.decorators import login_required
from .models import Kategoria, Produkt
from django.db.models import Avg
from oceny.models import Ocena
from django.contrib.auth import get_user_model, logout, login


User = get_user_model()

def lista_produktow(request, kategoria_skrot_url=None, msg=None):
    kategoria = None
    kategorie = Kategoria.objects.all()
    produkty = Produkt.objects.filter(dostepny=True)
    if kategoria_skrot_url:
        request.session["msg"]=""
        kategoria = get_object_or_404(Kategoria, skrot_url=kategoria_skrot_url)
        produkty = produkty.filter(kategoria=kategoria)
    return render(request,
                  'sklep/produkt/lista.html',
                  {'msg':msg,
                    'kategoria': kategoria,
                   'kategorie': kategorie,
                   'produkty': produkty})

#@login_required(login_url="/account/login/")
def znajdz_produkty(request):
    kategoria=None
    szukana_nazwa=None
    kategorie = Kategoria.objects.all()
    produkty = Produkt.objects.all()
    request.session["msg"]=""
    if request.method=="POST":
        szukana_nazwa = request.POST['szuknazwa']
        produkty = Produkt.objects.filter(nazwa__contains=szukana_nazwa)
    return render(request,
                  'sklep/produkt/lista.html',
                  {'szukane': szukana_nazwa,
                   'kategoria': kategoria,
                   'kategorie': kategorie,
                   'produkty': produkty})

def wyloguj(request):
    zalogowany_user = request.user
    kategoria=None
    kategorie = Kategoria.objects.all()
    produkty = Produkt.objects.all()
    
    if (zalogowany_user.is_authenticated):
        logout(request)
    return render(request,
                   'sklep/produkt/lista.html',
                   {'msg': 'Wylogowano pomyślnie',
                   'kategoria': kategoria,
                   'kategorie': kategorie,
                   'produkty': produkty})

def rejestracja(request):
    return render(request,'accounts/signup')


def privacy(request):
    return render(request,'sklep/privacy.html')

def o_nas(request):
    return render(request,'sklep/o_nas.html')

def kontakt(request):
    return render(request,'sklep/kontakt.html')

def zwroty(request):
    return render(request,'sklep/zwroty.html')

def zaloguj(request):
    
    zalogowany_user = request.user
    if (not zalogowany_user.is_authenticated):
        login(request)
    return render(request,'')
    

def szczegoly_produktu(request, id, skrot_url, kategoria_skrot_url=None):
    kategoria=None
    request.session["msg"]=""
    kategorie = Kategoria.objects.all()
    produkt = get_object_or_404(Produkt,
                                id=id,
                                skrot_url=skrot_url,
                                dostepny=True)
    oceny = Ocena.objects.filter(produkt__exact=id)
    srednia_ocena = oceny.aggregate(Avg('gwiazdki'))['gwiazdki__avg']
    if (not srednia_ocena is None):
        srednia_ocena_calk= int(srednia_ocena + 0.5)
        reszta = 5 - srednia_ocena_calk
    else:
        srednia_ocena_calk= 0
        reszta = 5 - srednia_ocena_calk
    formularz_dodaj_do_koszyka = FormularzDodajProduktDoKoszyka()

    if kategoria_skrot_url:
        kategoria = get_object_or_404(Kategoria, skrot_url=kategoria_skrot_url)

    return render(request,
                  'sklep/produkt/szczegoly.html',
                  {'kategoria': kategoria,
                   'kategorie': kategorie, 
                   'produkt': produkt,
                   'srednia_ocena':srednia_ocena,
                   'srednia_ocena_calk':srednia_ocena_calk,
                   'reszta':reszta,
                   'liczba_ocen':oceny.count(),
                   'formularz_dodaj_do_koszyka': formularz_dodaj_do_koszyka})
