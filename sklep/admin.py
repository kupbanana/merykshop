from django.contrib import admin
from .models import Kategoria, Produkt


@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'skrot_url']
    prepopulated_fields = {'skrot_url': ('nazwa',)}

@admin.register(Produkt)
class ProduktAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'skrot_url', 'cena',
                    'dostepny', 'utworzony', 'zaktualizowany']
    list_filter = ['dostepny', 'utworzony', 'zaktualizowany']
    list_editable = ['cena', 'dostepny']
    prepopulated_fields = {'skrot_url': ('nazwa',)}
