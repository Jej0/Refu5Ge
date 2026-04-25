from django.shortcuts import render
from django.db.models import Sum, Count
from .models import ObjetConnecte, Service, UtilisationObjet, HistoriqueDonnee


def dashboard(request):
    total_objets = ObjetConnecte.objects.count()

    objets_actifs = ObjetConnecte.objects.filter(statut="actif").count()
    objets_inactifs = ObjetConnecte.objects.filter(statut="inactif").count()

    total_services = Service.objects.count()
    total_utilisations = UtilisationObjet.objects.count()
    total_historiques = HistoriqueDonnee.objects.count()

    consommation_totale = UtilisationObjet.objects.aggregate(
        total=Sum("consommation")
    )["total"]

    if consommation_totale is None:
        consommation_totale = 0

    objet_plus_utilise = (
        UtilisationObjet.objects
        .values("objet__nom")
        .annotate(nombre=Count("id"))
        .order_by("-nombre")
        .first()
    )

    service_plus_utilise = (
        UtilisationObjet.objects
        .values("service__nom")
        .annotate(nombre=Count("id"))
        .order_by("-nombre")
        .first()
    )

    historiques_recents = (
        HistoriqueDonnee.objects
        .select_related("objet")
        .order_by("-date_mesure")[:5]
    )

    context = {
        "total_objets": total_objets,
        "objets_actifs": objets_actifs,
        "objets_inactifs": objets_inactifs,
        "total_services": total_services,
        "total_utilisations": total_utilisations,
        "total_historiques": total_historiques,
        "consommation_totale": consommation_totale,
        "objet_plus_utilise": objet_plus_utilise,
        "service_plus_utilise": service_plus_utilise,
        "historiques_recents": historiques_recents,
    }

    return render(request, "rapports/dashboard.html", context)


def rapport(request):
    utilisations = (
        UtilisationObjet.objects
        .select_related("objet", "service")
        .order_by("-date_utilisation")
    )

    consommation_totale = utilisations.aggregate(
        total=Sum("consommation")
    )["total"]

    if consommation_totale is None:
        consommation_totale = 0

    duree_totale = utilisations.aggregate(
        total=Sum("duree_minutes")
    )["total"]

    if duree_totale is None:
        duree_totale = 0

    context = {
        "utilisations": utilisations,
        "consommation_totale": consommation_totale,
        "duree_totale": duree_totale,
    }

    return render(request, "rapports/rapport.html", context)


def historique(request):
    historiques = (
        HistoriqueDonnee.objects
        .select_related("objet")
        .order_by("-date_mesure")
    )

    context = {
        "historiques": historiques,
    }

    return render(request, "rapports/historique.html", context)