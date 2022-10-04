from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('koszyk/', include('koszyk.urls', namespace='koszyk')),
    path('zamowienia/', include('zamowienia.urls', namespace='zamowienia')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('accounts/', include('allauth.urls')),
    path('', include('sklep.urls', namespace='sklep')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
