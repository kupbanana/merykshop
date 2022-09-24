from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
   path('stripe/', views.payment_with_stripe, name='stripe-payment'),
    path('payment-success/', views.payment_done, name='payment-success'),
    path('payment-cancel/', views.payment_canceled, name='payment-cancel'),
]
