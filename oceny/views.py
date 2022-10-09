from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse
from .models import Ocena
from sklep.models import Produkt
from zamowienia.models import PozycjaZamowienia, Zamowienie
from .forms import FormularzDodajOcene


def sprawdz_czy_uzytkownik_zamawial_ten_produkt(pozycje_zamowien, zalogowany_user, produkt_id):
    for pozycja in pozycje_zamowien:
        if pozycja.zamówienie.uzytkownik != zalogowany_user:
            continue
        if pozycja.produkt.id==produkt_id:
            return True        
    return False



def dodaj_ocene(request, produkt_id):
    #sprawdz czy użytkownik jest zalogowany
    zalogowany_user = request.user
    host = request.get_host()      
    produkt=Produkt.objects.get(id=produkt_id)  
    prefiks_strony="https://{}{}" if request.is_secure() else "http://{}{}"
    url = reverse('zamowienia:admin_order_pdf', args=[produkt_id])
    dodaj_ocene_url=prefiks_strony.format(host,reverse('oceny:dodaj-ocene-formularz', args=[produkt_id]))
    niezalogowany_url=prefiks_strony.format(host,reverse('oceny:uzytkownik-niezalogowany'))
    uzytkownik_tego_nie_zamawial_url=prefiks_strony.format(host,reverse('oceny:uzytkownik-tego-niezamawial', args=[produkt_id]))
    
    if (not zalogowany_user.is_authenticated):
        return redirect(niezalogowany_url, code=303)
    zamowienia_uzytkownika=Zamowienie.objects.filter(uzytkownik=zalogowany_user)
    pozycje_zamowien = get_list_or_404(PozycjaZamowienia)
    #produkty_uzytkownika=PozycjaZamowienia.objects.filter(zamówienie.uzytkownik)
    if (not sprawdz_czy_uzytkownik_zamawial_ten_produkt(pozycje_zamowien, zalogowany_user, produkt_id)):
        return redirect(uzytkownik_tego_nie_zamawial_url, code=304)


    if (request.method=='POST'):
        return dodaj_ocene_formularz(request, produkt)    
   
    formularz = FormularzDodajOcene() # pusty formularz
    return render(request,
                  'oceny/dodaj_ocene.html',
                  {'produkt': produkt, 'form': formularz})
    

def uzytkownik_niezalogowany(request):
    return render(request, 'oceny/niezalogowany.html')

def uzytkownik_nie_zamawial_produktu(request, produkt_id):
    produkt=Produkt.objects.get(id=produkt_id)  
    return render(request, 'oceny/niezamawiany_produkt.html', {'produkt': produkt})

def dodaj_ocene_formularz(request, produkt):
    
    formularz = FormularzDodajOcene(request.POST)
    if formularz.is_valid():
        # Utworz ocene na podstawie pól formularza
        ocena = Ocena()
        ocena.uzytkownik = request.user
        ocena.produkt = produkt
        ocena.gwiazdki=formularz.cleaned_data['gwiazdki']
        ocena.save()
        return render(request, 'oceny/ocena_sukces.html',{'produkt':produkt})
    return render(request, 'oceny/blad_ocena.html',{'produkt':produkt})
