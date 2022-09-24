from django.urls import path
from . import views

app_name = 'koszyk'

urlpatterns = [
    path('', views.koszyk_szczegoly, name='koszyk_szczegoly'),
    path('dodaj/<int:produkt_id>/', views.koszyk_dodaj, name='koszyk_dodaj'),
    path('usun/<int:produkt_id>/', views.koszyk_usun, name='koszyk_usun'),
]
