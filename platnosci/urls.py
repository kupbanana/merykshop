from django.urls import path
from . import views

app_name = 'platnosci'

urlpatterns = [
   path('stripe/', views.platnosc_przez_stripe, name='platnosc-stripe'),
    path('platnosc-sukces/', views.platnosc_wykonana, name='platnosc-sukces'),
    path('platnosc-anulowana/', views.platnosc_anulowana, name='platnosc-anulowana'),
]
