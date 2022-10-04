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
from uzytkownicy.models import UzytkownikProfil
from django.contrib.auth.models import User
from .forms import OrderCreateForm
from datetime import datetime
from allauth.socialaccount.models import SocialAccount
email_address=''

def is_social(request):
    return SocialAccount.objects.filter(user=request.user).exists()

def get_social_user(request):
    return SocialAccount.objects.filter(user=request.user)[0]


# imie = forms.CharField(max_length=50)
# nazwisko = forms.CharField(max_length=50)
# email = forms.EmailField()
# adres = forms.CharField(max_length=250)
# kod_pocztowy = forms.CharField(max_length=20)
# miasto = forms.CharField(max_length=100)

def utworz_zamowienie(request):
    koszyk = Koszyk(request)
    zalogowany_user = request.user
    init_data={}
    guest_user=get_object_or_404(User, last_name='Gość')
    #logout(request)
    if (zalogowany_user.is_authenticated):
        if (not is_social(request)): 
            profil = UzytkownikProfil.objects.get(user=zalogowany_user)
            init_data={"imie":  zalogowany_user.first_name, "nazwisko": zalogowany_user.last_name, "email": zalogowany_user.email, "adres":profil.adres, "kod_pocztowy":profil.kod_pocztowy, "miasto":profil.miasto }
        else:
            social_user=get_social_user(request)
            init_data={"imie":  zalogowany_user.first_name, "nazwisko": zalogowany_user.last_name, "email": social_user.extra_data['email'] }

    else:
        zalogowany_user=guest_user
        init_data={"imie":  zalogowany_user.first_name, "nazwisko": zalogowany_user.last_name, "email": "" }    
        # sprawdzic, czy None, jeśli tak, wypełnić pola zamówienia danymi gościa i pozwolić na wypełnienie pól formularza
        # jeśli nie None, to wypełnić formularz danymi użytkownika z bazy danych
    if (request.method=='POST'):
        form = OrderCreateForm(request.POST,initial=init_data)
        #form = OrderCreateForm(initial={"imie":  zalogowany_user.first_name, "nazwisko": zalogowany_user.last_name, "email": zalogowany_user.email, "adres":profil.adres, "kod_pocztowy":profil.kod_pocztowy, "miasto":profil.miasto })
        if form.is_valid():
            # Utworz zamowienie na podstawie pól formularza
            #Subject(subject_id=1, name='Physics', max_marks=100)
            
            zamowienie = Zamowienie(uzytkownik=zalogowany_user,utworzone=datetime.now())
            zamowienie.email = form.cleaned_data['email']
            zamowienie.adres = form.cleaned_data['adres']
            zamowienie.kod_pocztowy = form.cleaned_data['kod_pocztowy']
            zamowienie.miasto = form.cleaned_data['miasto']
            zamowienie.save()
            for towar in koszyk:
                PozycjaZamowienia.objects.create(zamówienie=zamowienie,
                                         produkt=towar['produkt'],
                                         cena=towar['cena'],
                                         ilosc=towar['ilosc'])
            # wyczyść koszyk
            koszyk.wyczysc()
            # wyślij e-maila
            zamowienie_utworzone(zamowienie.id)
            # ustaw zamówienie w sesji
            request.session['order_id'] = zamowienie.id
            # przekieruj płatność
            return redirect(reverse('payment:stripe-payment'))
    else:
        form = OrderCreateForm(initial=init_data)
    return render(request,
                  'zamowienia/zamowienie/utworz.html',
                  {'koszyk': koszyk, 'form': form})

def zamowienie_utworzone(id_zamowienia):
    """
    Wyślij e-mail z powiadomieniem o przyjęciu zamówienia.
    """
    zamowienie = Zamowienie.objects.get(id=id_zamowienia)
    subject = f'Zamówienie nr: {zamowienie.id}'
    message = f'Drogi {zamowienie.uzytkownik.first_name},\n\n' \
              f'Właśnie pomyślnie złożyłeś zamówienie. ' \
              f'Identyfikator Twojego zamówienia to: {zamowienie.id}.'
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_DISPLAY_NAME,
                          [zamowienie.email])
    return mail_sent




@staff_member_required
def admin_order_detail(request, id_zamowienia):
    zamowienie = get_object_or_404(Zamowienie, id=id_zamowienia)
    return render(request,
                  'admin/zamowienia/zamowienie/szczegoly.html',
                  {'zamowienie': zamowienie})


@staff_member_required
def admin_order_pdf(request, id_zamowienia):
    zamowienie = get_object_or_404(Zamowienie, id=id_zamowienia)
    html = render_to_string('zamowienia/zamowienie/pdf.html',
                            {'zamowienie': zamowienie})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{zamowienie.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response
