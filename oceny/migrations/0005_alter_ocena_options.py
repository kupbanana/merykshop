# Generated by Django 4.1.2 on 2022-10-09 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oceny', '0004_rename_product_ocena_produkt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ocena',
            options={'verbose_name': 'Ocena', 'verbose_name_plural': 'Oceny'},
        ),
    ]
