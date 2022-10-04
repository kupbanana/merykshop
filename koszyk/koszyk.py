from decimal import Decimal
from django.conf import settings
from sklep.models import Produkt


class Koszyk(object):

    def __init__(self, request):
        """
        Zainicjuj koszyk.
        """
        self.session = request.session
        koszyk = self.session.get(settings.CART_SESSION_ID)
        if not koszyk:
            # zapisz w sesji pusty koszyk
            koszyk = self.session[settings.CART_SESSION_ID] = {}
        self.koszyk = koszyk

    def __iter__(self):
        """
        Iteruj po towarach w koszyku i pobieraj produkty z
        bazy danych.
        """
        id_produktow = self.koszyk.keys()
        # pobierz obiekty produktów i dodaj je do koszyka
        produkty = Produkt.objects.filter(id__in=id_produktow)

        koszyk = self.koszyk.copy()
        for produkt in produkty:
            koszyk[str(produkt.id)]['produkt'] = produkt

        for towar in koszyk.values():
            towar['cena'] = Decimal(towar['cena'])
            towar['cena_razem'] = towar['cena'] * towar['ilosc']
            yield towar

    def __len__(self):
        """
        Zlicz towary w koszyku.        
        """
        suma=0
        try:
            suma = sum(towar['ilosc'] for towar in self.koszyk.values())
        except:
            self.wyczysc()
            pass
 
        return sum(towar['ilosc'] for towar in self.koszyk.values())

    def dodaj(self, produkt, ilosc=1, nadpisz_ilosc=False):
        """
        Dodaj produkt do koszyka lub zaktualizuj ilość.        """

        produkt_id = str(produkt.id)
        if produkt_id not in self.koszyk:
            self.koszyk[produkt_id] = {'ilosc': 0,
                                      'cena': str(produkt.cena)}
        if nadpisz_ilosc:
            self.koszyk[produkt_id]['ilosc'] = ilosc
        else:
            self.koszyk[produkt_id]['ilosc'] += ilosc
        self.zapisz()

    def zapisz(self):
        # oznacz sesję jako "modified", aby zyskać pewność, że zostanie zapisana
        self.session.modified = True

    def usun(self, produkt):
        """
        Usuwa produkt z koszyka.
        """
        produkt_id = str(produkt.id)
        if produkt_id in self.koszyk:
            del self.koszyk[produkt_id]
            self.zapisz()

    def wyczysc(self):
        # usuń koszyk z sesji
        self.koszyk.clear()
        

        del self.session[settings.CART_SESSION_ID]
        self.zapisz()

    def oblicz_laczna_cene(self):
        return sum(Decimal(towar['cena']) * towar['ilosc'] for towar in self.koszyk.values())
