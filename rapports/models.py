from django.db import models


class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    marque = models.CharField(max_length=50)
    statut = models.CharField(max_length=20)
    zone = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Service(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom


class UtilisationObjet(models.Model):
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_utilisation = models.DateTimeField()
    duree_minutes = models.IntegerField()
    consommation = models.FloatField()

    def __str__(self):
        return f"{self.objet.nom} - {self.date_utilisation}"


class HistoriqueDonnee(models.Model):
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    date_mesure = models.DateTimeField()
    type_donnee = models.CharField(max_length=50)
    valeur = models.FloatField()
    unite = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.objet.nom} - {self.type_donnee}"