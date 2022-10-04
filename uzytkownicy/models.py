from django.db import models
from django.contrib.auth.models import User

class UzytkownikProfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adres = models.CharField(max_length=250)
    kod_pocztowy = models.CharField(max_length=20)
    miasto = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="ProfileUżytkowników"

