# Generated by Django 4.1.2 on 2022-10-08 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zamowienia', '0007_zamowienie_imie_zamowienie_nazwisko'),
    ]

    operations = [
        migrations.AddField(
            model_name='zamowienie',
            name='gosc',
            field=models.BooleanField(default=True),
        ),
    ]
