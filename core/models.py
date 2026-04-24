from django.db import models

# Create your models here. Models are to get information from database
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator



class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')
    def __str__(self):
        return f"{self.name}"

class DeviceAttribute(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="attributes")
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

class CategorieObjet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.nom

class ObjetConnecte(models.Model):
    ETAT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('maintenance', 'En maintenance'),
    ]
    identifiant_unique = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(CategorieObjet, on_delete=models.SET_NULL, null=True, related_name='objets')
    marque = models.CharField(max_length=100, blank=True)
    modele = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='actif')
    batterie = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)
    temperature_actuelle = models.FloatField(null=True, blank=True)
    connectivite = models.CharField(max_length=50, blank=True)
    temperature_cible = models.FloatField(null=True, blank=True)
    piece = models.CharField(max_length=100, blank=True)
    date_installation = models.DateTimeField(default=timezone.now)
    derniere_interaction = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.nom} ({self.identifiant_unique})"
    class Meta:
        ordering = ['nom']

class Animal(models.Model):
    nom = models.CharField(max_length=100)
    espece = models.CharField(max_length=50)
    race = models.CharField(max_length=100, blank=True)
    age_estime = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='animaux/', blank=True)
    disponible_adoption = models.BooleanField(default=True)
    def __str__(self):
        return self.nom

class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateField()
    contenu = models.TextField()
    def __str__(self):
        return self.titre
