from django.contrib.auth.models import AbstractUser
from django.db import models

class Membre(AbstractUser):
    TYPE_CHOICES = [
        ('benevole', 'Bénévole'),
        ('soignant', 'Soignant'),
        ('veterinaire', 'Vétérinaire'),
        ('directeur', 'Directeur'),
    ]
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
    ]
    
    type_membre = models.CharField(max_length=50, choices=TYPE_CHOICES, default='benevole')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default='debutant')
    points = models.FloatField(default=0)
    email_valide = models.BooleanField(default=False)