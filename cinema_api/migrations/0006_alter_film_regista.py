# Generated by Django 4.2 on 2023-04-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cinema_api", "0005_film_regista_film_uscita"),
    ]

    operations = [
        migrations.AlterField(
            model_name="film",
            name="regista",
            field=models.TextField(max_length=20),
        ),
    ]