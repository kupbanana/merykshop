# Generated by Django 4.1.2 on 2022-10-08 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zamowienia', '0006_auto_20221001_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='zamowienie',
            name='imie',
            field=models.CharField(default='Gość', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zamowienie',
            name='nazwisko',
            field=models.CharField(default='Gość', max_length=50),
            preserve_default=False,
        ),
    ]
