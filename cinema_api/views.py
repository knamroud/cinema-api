from . import models
from . import serializers
from decimal import Decimal
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsGestore


class CinemaView(generics.ListCreateAPIView):
    queryset = models.Cinema.objects.all()
    serializer_class = serializers.CinemaSerializer
    pagination_class = None

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsAdminUser()]

    def list(self, request, *args, **kwargs):
        try:
            latitudine = Decimal(request.query_params.get("latitudine"))
            longitudine = Decimal(request.query_params.get("longitudine"))
            distanza_max = Decimal(request.query_params.get("distanza_max"))
            distanza_min = Decimal(request.query_params.get("distanza_min"))
        except:
            return Response({"detail": "Missing or invalid query fields."}, status.HTTP_400_BAD_REQUEST)
        data = []
        for cinema in self.get_queryset():
            distanza = Decimal(cinema.distance(
                Decimal(latitudine), Decimal(longitudine)))
            if distanza_max >= distanza and distanza >= distanza_min:
                data.append(cinema)
        return Response(self.serializer_class(data, many=True).data, status.HTTP_200_OK)


class SingleCinemaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Cinema.objects.all()
    serializer_class = serializers.CinemaSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsGestore() | IsAdminUser()]


class ProiezioneView(generics.ListCreateAPIView):
    serializer_class = serializers.ProiezioneSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsGestore() | IsAdminUser()]

    def get_queryset(self):
        if self.request.method == "GET":
            return models.Proiezione.objects.all()
        else:
            return models.Proiezione.objects.all().order_by("inizio") if IsAdminUser().has_permission(self.request, self) \
                else models.Proiezione.objects.filter(sala__cinema__in=[gestione.cinema for gestione in models.Gestore.objects.filter(gestore=self.request.user)]).order_by("inizio")


class SingleProiezioneView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Proiezione.objects.all()
    serializer_class = serializers.ProiezioneSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsGestore() | IsAdminUser()]

    def get_queryset(self):
        if self.request.method == "GET":
            return models.Proiezione.objects.all()
        else:
            return models.Proiezione.objects.all() if IsAdminUser().has_permission(self.request, self) \
                else models.Proiezione.objects.filter(sala__cinema__in=[gestione.cinema for gestione in models.Gestore.objects.filter(gestore=self.request.user)])


class SalaView(generics.ListCreateAPIView):
    queryset = models.Sala.objects.all().order_by("cinema", "numero") 
    serializer_class = serializers.SalaSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsAdminUser()]


class SingleSalaView(generics.RetrieveDestroyAPIView):
    queryset = models.Sala.objects.all()
    serializer_class = serializers.SalaSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsGestore() | IsAdminUser()]


class FilmView(generics.ListCreateAPIView):
    queryset = models.Film.objects.all().order_by("nome")
    serializer_class = serializers.FilmSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsAdminUser()]


class SingleFilmView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Film.objects.all()
    serializer_class = serializers.FilmSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsAdminUser()]


class CinemaProiezioneView(generics.ListCreateAPIView):
    serializer_class = serializers.ProiezioneSerializer

    def get_permissions(self):
        return [IsAuthenticated() if self.request.method == "GET" else IsGestore() | IsAdminUser()]

    def get_queryset(self):
        return models.Proiezione.objects.filter(cinema=self.request.kwargs["cinema"])


class PrenotazioneView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PrenotazioneSerializer

    def get_queryset(self):
        return models.Prenotazione.objects.all().order_by("posto")  if IsAdminUser().has_permission(self.request, self) \
            else models.Prenotazione.objects.filter(proiezione__sala__cinema__in=[gestione.cinema for gestione in models.Gestore.objects.filter(gestore=self.request.user)]).order_by("posto")  if IsGestore().has_permission(self.request, self) \
            else models.Prenotazione.objects.filter(utente=self.request.user).order_by("posto") 

    def perform_create(self, serializer):
        proiezione = models.Proiezione.objects.get(
            pk=self.request.data["proiezione_id"])
        prenotazioni = models.Prenotazione.objects.filter(
            proiezione=proiezione)
        posto = None
        last = 0
        assert prenotazioni.count() < proiezione.sala.posti, "Full"
        for p in prenotazioni:
            if p.posto > last+1:
                posto = last+1
                break
            last = p.posto
        posto = posto if posto else prenotazioni.count() + 1
        serializer.save(posto=posto, utente=self.request.user,
                        proiezione=proiezione)


class SinglePrenotazioneView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PrenotazioneSerializer

    def get_queryset(self):
        return models.Prenotazione.objects.all() if IsAdminUser().has_permission(self.request, self) \
            else models.Prenotazione.objects.filter(proiezione__sala__cinema__in=[gestione.cinema for gestione in models.Gestore.objects.filter(gestore=self.request.user)]) if IsGestore().has_permission(self.request, self) \
            else models.Prenotazione.objects.filter(utente=self.request.user)
