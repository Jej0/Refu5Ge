from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="rapports_dashboard"),
    path("rapport/", views.rapport, name="rapports_rapport"),
    path("historique/", views.historique, name="rapports_historique"),
    path("optimisation/", views.optimisation, name="rapports_optimisation"),
]