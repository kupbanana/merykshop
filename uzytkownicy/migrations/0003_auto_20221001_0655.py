# Generated by Django 3.0.14 on 2022-10-01 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uzytkownicy', '0002_uzytkownik_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uzytkownik',
            name='login',
        ),
        migrations.AddField(
            model_name='uzytkownik',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
