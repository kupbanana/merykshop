go.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from zamowienia.models import Zamowienie
from django.urls import reverse
import weasyprint
from io import BytesIO
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import stripe

def payment_done(request):
    order_id = request.session.get('order_id')
    order = Zamowienie.objects.get(id=order_id)
    order.zaplacone = True
    order.save()
    platnosc_zakonczona(order_id)
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_with_stripe(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    host = request.get_host()        
    order_id = request.session.get('order_id')
    payment_method = request.session.get('stripe_method')
    order = Zamowienie.objects.get(id=order_id)
    amount = int(round(order.oblicz_laczna_kwote()*100))
    page_prefix="https://{}{}" if request.is_secure() else "http://{}{}"

    checkout_session = stripe.checkout.Session.create(
        
        payment_method_types=['card', 'blik'],    
        customer_email=order.email,    
        line_items=[
            {               
                'price_data': {
                    'currency': 'PLN',
                    'unit_amount': amount,
                    'product_data': {
                        'name': f'Zamówienie nr: {order.id}, ({order.lista_towarow()})',                        
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=page_prefix.format(host,reverse('payment:payment-success')),
        cancel_url=page_prefix.format(host,reverse('payment:payment-cancel')),
    )   
    return redirect(checkout_session.url, code=303)



def platnosc_zakonczona(order_id):
    """
    Wyślij e-mail po pomyślnej płatności.
    """
    order = Zamowienie.objects.get(id=order_id)

    # stwórz e-maila z fakturą
    subject = f'Sklep Eweliny - Faktura nr:  {order.id}'
    message = 'W załączeniu faktura za Twój ostatni zakup.'
    email = EmailMessage(subject,
                         message,
                         settings.EMAIL_DISPLAY_NAME,
                         [order.email])
    # wygeneruj PDF
    html = render_to_string('zamowienia/zamowienie/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    # dołącz plik PDF
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    
    # syślij e-mail
    email.send()


