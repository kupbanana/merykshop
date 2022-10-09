from django.db import models
from sklep.models import Produkt
from django.contrib.auth.models import User


class Zamowienie(models.Model):
    uzytkownik = models.ForeignKey(User,
                              related_name='uzytkownik',
                              on_delete=models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    email = models.EmailField(default=None)
    adres = models.CharField(default='', max_length=250)
    kod_pocztowy = models.CharField(default='', max_length=20)
    miasto = models.CharField(default='', max_length=100)
    utworzone = models.DateTimeField(auto_now_add=True)
    zaktualizowane = models.DateTimeField(auto_now=True)
    zaplacone = models.BooleanField(default=False)
    gosc = models.BooleanField(default=True)
    id_serwisu_platniczego = models.CharField(max_length=150, blank=True)

    class Meta:
        
        ordering = ('-utworzone',)
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamówienia'
       

    def __str__(self):
        return f'Zamowienie {self.id}'
    
    def lista_towarow(self):
        s=''
        for item in self.artykuly.all():
            s+=f'{item.produkt.nazwa} x {item.ilosc}, '
        if (len(s)>150):
            s=s[0:149]+'...'
        if s.endswith(', '):
            s=s[:-2]
        return s

    def oblicz_laczna_kwote(self):
        return sum(item.oblicz_cene() for item in self.artykuly.all())


class PozycjaZamowienia(models.Model):
    zamówienie = models.ForeignKey(Zamowienie,
                              related_name='artykuly',
                              on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt,
                                related_name='pozycje_zamowienia',
                                on_delete=models.CASCADE)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    ilosc = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def oblicz_cene(self):
        return self.cena * self.ilosc
