from django.shortcuts import render
from .models import Animal, Actualite, ObjetConnecte, CategorieObjet

# Module Information (visiteur)

def accueil(request):
    animaux = Animal.objects.filter(disponible_adoption=True)[:6]
    objets = ObjetConnecte.objects.all().order_by('-derniere_interaction')[:4]
    # actualites = Actualite.objects.order_by('-date')[:3]  # facultatif
    context = {
        'animaux': animaux,
        'objets': objets,
        # 'actualites': actualites,
    }
    return render(request, 'core/accueil.html', context)

def recherche(request):
    """Recherche avec au moins 2 filtres pour animaux et objets"""
    animaux = Animal.objects.all()
    objets = ObjetConnecte.objects.all()
    especes_disponibles = Animal.objects.values_list('espece', flat=True).distinct()
    races_disponibles = Animal.objects.values_list('race', flat=True).distinct()
    categories = CategorieObjet.objects.all()

    # Filtres animaux
    nom = request.GET.get('nom')
    espece = request.GET.get('espece')
    race = request.GET.get('race')
    if nom:
        animaux = animaux.filter(nom__icontains=nom)
    if espece:
        animaux = animaux.filter(espece__icontains=espece)
    if race:
        animaux = animaux.filter(race__icontains=race)

    # Filtres objets
    objet_nom = request.GET.get('objet_nom')
    categorie = request.GET.get('categorie')
    if objet_nom:
        objets = objets.filter(nom__icontains=objet_nom)
    if categorie:
        objets = objets.filter(categorie_id=categorie)

    context = {
        'animaux': animaux,
        'objets': objets,
        'especes_disponibles': especes_disponibles,
        'races_disponibles': races_disponibles,
        'categories': categories,
    }
    return render(request, 'core/recherche.html', context)
