from django.urls import path
from . import views

app_name = 'zamowienia'

urlpatterns = [
    path('utworz/', views.utworz_zamowienie, name='utworz_zamowienie'),
    path('admin/zamowienie/<int:id_zamowienia>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/zamowienie/<int:id_zamowienia>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    
]
