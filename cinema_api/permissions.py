from rest_framework.permissions import BasePermission
from .models import Gestore, Cinema, Proiezione, Prenotazione


class IsGestore(BasePermission):

    def has_permission(self, request, view):
        return True if bool(request.user and request.user.is_authenticated) and \
            Gestore.objects.all().filter(gestore=request.user) else False

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        cinema = obj if isinstance(obj, Cinema) else obj.sala.cinema if isinstance(
            obj, Proiezione) else obj.proiezione.sala.cinema
        return True if len(Gestore.objects.filter(gestore=request.user, cinema=cinema)) else False
