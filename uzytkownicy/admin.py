from django.contrib import admin
from .models import UzytkownikProfil

# Register your models here.
#   user = models.OneToOneField(User, on_delete=models.CASCADE)
#   adres = models.CharField(max_length=250)
#   kod_pocztowy = models.CharField(max_length=20)
#   miasto = models.CharField(max_length=100)

@admin.register(UzytkownikProfil)
class UzytkownikProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'adres', 'kod_pocztowy', 'miasto']
    list_filter =  ['adres', 'kod_pocztowy', 'miasto']
    list_editable = ['adres','kod_pocztowy', 'miasto']
    
