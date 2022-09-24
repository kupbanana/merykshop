import weasyprint
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
import weasyprint
from io import BytesIO
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from koszyk.koszyk import Koszyk
from .models import PozycjaZamowienia, Zamowienie
from .forms import OrderCreateForm


def order_create(request):
    koszyk = Koszyk(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            zamowienie = form.save()
            for towar in koszyk:
                PozycjaZamowienia.objects.create(zamówienie=zamowienie,
                                         produkt=towar['produkt'],
                                         cena=towar['cena'],
                                         ilosc=towar['ilosc'])
            # wyczyść koszyk
            koszyk.wyczysc()
            # wyślij e-maila
            order_created(zamowienie.id)
            # ustaw zamówienie w sesji
            request.session['order_id'] = zamowienie.id
            # przekieruj płatność
            return redirect(reverse('payment:stripe-payment'))
           
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'koszyk': koszyk, 'form': form})

def order_created(order_id):
    """
    Wyślij e-mail z powiadomieniem o przyjęciu zamówienia.
    """
    order = Zamowienie.objects.get(id=order_id)
    subject = f'Zamówienie nr: {order.id}'
    message = f'Drogi {order.imie},\n\n' \
              f'Właśnie pomyślnie złożyłeś zamówienie. ' \
              f'Identyfikator Twojego zamówienia to: {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_DISPLAY_NAME,
                          [order.email])
    return mail_sent




@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Zamowienie, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response
