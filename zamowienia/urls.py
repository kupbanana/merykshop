from django.urls import path
from . import views

app_name = 'zamowienia'

urlpatterns = [
    path('utworz/', views.utworz_zamowienie, name='utworz_zamowienie'),
    path('moje-zamowienia/',views.zamowienia_uzytkownika, name='wyswietl-zamowienia-uzytkownika'),
    path('admin/zamowienie/<int:id_zamowienia>/', views.admin_order_detail, name='admin_order_detail'),
    path('zamowienie/<int:id_zamowienia>/', views.szczegoly_zamowienia, name='szczegoly_zamowienia'),
    path('admin/zamowienie/<int:id_zamowienia>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    
]
