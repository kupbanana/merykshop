from django.db import models
from uzytkownicy.models import UzytkownikProfil
from sklep.models import Produkt
from django.core.validators import MaxValueValidator, MinValueValidator


class Ocena(models.Model):
    product = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    uzytkownik = models.ForeignKey(UzytkownikProfil, on_delete=models.CASCADE)
    gwiazdki = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return str(self.product)+"---"+str(self.user)
