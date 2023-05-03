from django.db import models
import math
from django.contrib.auth.models import User


class Cinema(models.Model):
    nome = models.TextField(max_length=20)
    longitudine = models.DecimalField(
        db_index=True, max_digits=20, decimal_places=17)
    latitudine = models.DecimalField(
        db_index=True, max_digits=20, decimal_places=17)

    def __str__(self):
        return self.nome

    def distance(self, lat, lon):
        dlat = math.radians(self.latitudine - lat)
        dlon = math.radians(self.longitudine - lon)
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(self.latitudine)) * math.cos(math.radians(lat)) *
             math.sin(dlon/2) * math.sin(dlon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return 6371 * c

    class Meta:
        unique_together = ("longitudine", "latitudine")


class Gestore(models.Model):
    cinema = models.ForeignKey(Cinema, models.CASCADE)
    gestore = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return f"{self.gestore.username}, {self.cinema.nome}"

    class Meta:
        unique_together = ("cinema", "gestore")


class Sala(models.Model):
    cinema = models.ForeignKey(Cinema, models.CASCADE)
    numero = models.PositiveSmallIntegerField()
    posti = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cinema.nome}, sala {self.numero}"

    class Meta:
        unique_together = ("cinema", "numero")


class Film(models.Model):
    nome = models.TextField(max_length=30)
    uscita = models.DateField()
    regista = models.TextField(max_length=20)

    def __str__(self):
        return self.nome


class Proiezione(models.Model):
    film = models.ForeignKey(Film, models.CASCADE)
    sala = models.ForeignKey(Sala, models.CASCADE)
    inizio = models.DateTimeField()
    is3d = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.sala)}: {self.film}"

    class Meta:
        unique_together = ("sala", "inizio")


class Prenotazione(models.Model):
    utente = models.ForeignKey(User, models.CASCADE)
    proiezione = models.ForeignKey(Proiezione, models.CASCADE)
    posto = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.utente}, {str(self.proiezione)}"
