# Generated by Django 3.0.14 on 2022-10-01 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uzytkownicy', '0004_auto_20221001_0906'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oceny', '0002_auto_20221001_0906'),
        ('zamowienia', '0004_auto_20221001_0906'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Uzytkownik',
        ),
        migrations.AddField(
            model_name='uzytkownikprofil',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
