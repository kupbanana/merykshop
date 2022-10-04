from django.db import models
from django.urls import reverse


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=200,
                            db_index=True)
    skrot_url = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('nazwa',)
        verbose_name = 'kategoria'
        verbose_name_plural = 'kategorie'

    def __str__(self):
        return self.nazwa

    def get_absolute_url(self):
        return reverse('sklep:lista_produktow_wg_kategorii',
                       args=[self.skrot_url])


class Produkt(models.Model):
    kategoria = models.ForeignKey(Kategoria,
                                 related_name='produkty',
                                 on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=200, db_index=True)
    skrot_url = models.SlugField(max_length=200, db_index=True)
    zdjecie = models.ImageField(upload_to='Produkty/%Y/%m/%d',
                              blank=True)
    opis = models.TextField(blank=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    dostepny = models.BooleanField(default=True)
    utworzony = models.DateTimeField(auto_now_add=True)
    zaktualizowany = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nazwa',)
        verbose_name = "artykuł"
        verbose_name_plural = "artykuły"
        index_together = (('id', 'skrot_url'),)

    def __str__(self):
        return self.nazwa

    def get_absolute_url(self):
        return reverse('sklep:szczegoly_produktu',
                       args=[self.id, self.skrot_url])



