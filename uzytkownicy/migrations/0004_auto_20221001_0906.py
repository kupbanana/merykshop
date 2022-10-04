# Generated by Django 3.0.14 on 2022-10-01 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uzytkownicy', '0003_auto_20221001_0655'),
    ]

    operations = [
        migrations.CreateModel(
            name='UzytkownikProfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adres', models.CharField(max_length=250)),
                ('kod_pocztowy', models.CharField(max_length=20)),
                ('miasto', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'ProfileUżytkowników',
            },
        ),
        migrations.RemoveField(
            model_name='uzytkownik',
            name='user',
        ),
    ]