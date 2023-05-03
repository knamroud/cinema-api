from rest_framework import serializers
from . import models


class CinemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cinema
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("longitudine", "latitudine"),
                message=("Posto già occupato.")
            )
        ]


class SalaSerializer(serializers.ModelSerializer):
    cinema_id = serializers.IntegerField(write_only=True)
    cinema = serializers.StringRelatedField(read_only=True)
    posti = serializers.IntegerField()

    class Meta:
        model = models.Sala
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("cinema", "numero"),
                message=("Sala già esistente.")
            )
        ]


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Film
        fields = "__all__"


class ProiezioneSerializer(serializers.ModelSerializer):
    film_id = serializers.IntegerField(write_only=True)
    film = serializers.StringRelatedField(read_only=True)
    sala_id = serializers.IntegerField(write_only=True)
    sala = serializers.StringRelatedField(read_only=True)
    is3d = serializers.BooleanField()

    class Meta:
        model = models.Proiezione
        fields = "__all__"
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("sala_id", "inizio"),
                message=("Sala già occupata.")
            )
        ]


class PrenotazioneSerializer(serializers.ModelSerializer):
    utente = serializers.SerializerMethodField("get_username", read_only=True)
    posto = serializers.IntegerField(required=False)
    proiezione_id = serializers.IntegerField(write_only=True)
    proiezione = serializers.StringRelatedField(read_only=True)

    def get_username(self, obj):
        return obj.utente.username

    class Meta:
        model = models.Prenotazione
        fields = "__all__"
