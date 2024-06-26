from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin
from . import views

app_name = 'sklep'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/',views.wyloguj, name='logout'),
    path('accounts/login/',views.zaloguj, name='login'),
    path('accounts/signup/',views.rejestracja, name='rejestracja'),    
    path ('privacy/',views.privacy, name ='privacy'),
    path ('o_nas/',views.o_nas, name ='o_nas'),
    path ('kontakt/',views.kontakt, name ='kontakt'),
    path ('zwroty/',views.zwroty, name ='zwroty'),
    path('account/', include('allauth.urls')),
    path('', views.lista_produktow, name='lista_produktow'),
    path('znajdz_produkty/', views.znajdz_produkty, name = 'znajdz_produkty'),
    path('<slug:kategoria_skrot_url>/', views.lista_produktow, name='lista_produktow_wg_kategorii'),
    path('<int:id>/<slug:skrot_url>/', views.szczegoly_produktu, name='szczegoly_produktu'),
]
