from django.urls import path
from . import views

app_name = 'zamowienia'

urlpatterns = [
    path('utworz/', views.utworz_zamowienie, name='utworz_zamowienie'),
    path('admin/zamowienie/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/zamowienie/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    
]
