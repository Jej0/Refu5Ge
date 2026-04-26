from django.urls import path
from . import views

urlpatterns = [
    path("", views.rapports_accueil, name="rapports_accueil"),
    path("global/", views.rapport_global, name="rapport_global"),
    path("piece/<int:room_id>/", views.rapport_piece, name="rapport_piece"),
    path("piece/<int:room_id>/csv/", views.export_room_csv, name="export_room_csv"),
    path("historique/", views.historique, name="rapports_historique"),
    path("maintenance/", views.maintenance, name="rapports_maintenance"),
]