# Generated by Django 4.2 on 2023-04-19 14:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cinema_api", "0003_sala_posti_massimi_alter_prenotazione_posto_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sala",
            old_name="posti_massimi",
            new_name="posti",
        ),
    ]