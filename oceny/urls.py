from django.urls import path
from . import views

app_name = 'oceny'

urlpatterns = [
    path('dodaj_ocene/<int:produkt_id>/', views.dodaj_ocene, name='dodaj-ocene'),
    path('uzytkownik_niezalogowany/', views.uzytkownik_niezalogowany, name='uzytkownik-niezalogowany'),  
    path('uzytkownik_niezamawial/<int:produkt_id>', views.uzytkownik_nie_zamawial_produktu, name='uzytkownik-tego-niezamawial'),    
    path('dodaj_ocene_f/<int:produkt_id>', views.dodaj_ocene_formularz, name='dodaj-ocene-formularz'),    
]
