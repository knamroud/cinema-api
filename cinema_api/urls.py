from django.urls import path
from . import views

urlpatterns = [
    path("cinema", views.CinemaView.as_view()),
    path("cinema/<int:pk>", views.SingleCinemaView.as_view()),
    path("cinema/<int:cinema>/proiezioni",
         views.CinemaProiezioneView.as_view()),
    path("proiezioni", views.ProiezioneView.as_view()),
    path("proiezioni/<int:pk>", views.SingleProiezioneView.as_view()),
    path("prenotazioni", views.PrenotazioneView.as_view()),
    path("prenotazioni/<int:pk>", views.SinglePrenotazioneView.as_view()),
]
