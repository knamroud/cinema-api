# Generated by Django 4.2 on 2023-04-19 14:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("cinema_api", "0004_rename_posti_massimi_sala_posti"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="regista",
            field=models.TextField(default="cio"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="film",
            name="uscita",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
