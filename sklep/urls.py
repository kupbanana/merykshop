from django.urls import path
from . import views

app_name = 'sklep'

urlpatterns = [
    path('', views.lista_produktow, name='lista_produktow'),
    path('znajdz_produkty/', views.znajdz_produkty, name = 'znajdz_produkty'),
    path('<slug:kategoria_skrot_url>/', views.lista_produktow, name='lista_produktow_wg_kategorii'),
    path('<int:id>/<slug:skrot_url>/', views.szczegoly_produktu, name='szczegoly_produktu'),
]
