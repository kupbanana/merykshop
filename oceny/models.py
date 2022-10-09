from django.db import models
from django.contrib.auth.models import User
from sklep.models import Produkt
from django.core.validators import MaxValueValidator, MinValueValidator


class Ocena(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    gwiazdki = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Ocena'
        verbose_name_plural = 'Oceny'
    def __str__(self):
        return str(self.produkt)+"---"+str(self.uzytkownik)+"----"+str(self.gwiazdki)
