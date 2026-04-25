from django.contrib import admin
from .models import ObjetConnecte, Service, UtilisationObjet, HistoriqueDonnee

admin.site.register(ObjetConnecte)
admin.site.register(Service)
admin.site.register(UtilisationObjet)
admin.site.register(HistoriqueDonnee)