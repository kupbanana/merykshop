# Generated by Django 3.0.14 on 2022-10-01 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zamowienia', '0005_auto_20221001_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zamowienie',
            name='uzytkownik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uzytkownik', to=settings.AUTH_USER_MODEL),
        ),
    ]
