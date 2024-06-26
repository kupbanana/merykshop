import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Zamowienie, PozycjaZamowienia


class PozycjaZamowieniaInline(admin.TabularInline):
    model = PozycjaZamowienia
    raw_id_fields = ['produkt']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many\
    and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Eksport do CSV'


def order_detail(obj):
    url = reverse('zamowienia:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">Podgląd</a>')

def order_pdf(obj):
    url = reverse('zamowienia:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Faktura'

@admin.register(Zamowienie)
class OrderAdmin(admin.ModelAdmin):
    #list_display = ['id', 'uzykownik.imie', 'uzytkownik.nazwisko', 'uzytkownik.email',
    #                'uzytkownik.adres', 'uzytkownik.kod_pocztowy', 'uzytkownik.miasto', 'zaplacone',
    #                'utworzone', 'zaktualizowane', order_detail, order_pdf]
    list_display = ['id', 'uzytkownik', 'zaplacone',
                    'utworzone', 'zaktualizowane', order_detail, order_pdf]
    list_filter = ['zaplacone', 'utworzone', 'zaktualizowane']
    inlines = [PozycjaZamowieniaInline]
    actions = [export_to_csv]
