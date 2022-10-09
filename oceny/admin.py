from django.contrib import admin
from .models import Ocena


@admin.register(Ocena)
class OcenaAdmin(admin.ModelAdmin):
    list_display = ['uzytkownik', 'produkt', 'gwiazdki']
    list_filter = ['uzytkownik', 'produkt']
    
