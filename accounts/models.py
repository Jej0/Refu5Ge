from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Table qui stocke les token pour verif le mail
class EmailVerifToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 86400

class UserProfile(models.Model):
    BASIC = 'basic'
    ADVANCED = 'advanced'
    MANAGER = 'manager'
    LEVEL_CHOICES = [
        (BASIC, 'Utilisateur simple'),
        (ADVANCED, 'Utilisateur avancé'),
        (MANAGER, 'Gestionnaire'),
    ]

    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Champs Module 2 (Nettoyés)
    age = models.PositiveIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    type_membre = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    points = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=BASIC)

    def check_level_up(self):
        if self.points >= 50 and self.level == self.BASIC:
            self.level = self.ADVANCED
            self.save(update_fields=['level'])
        elif self.points >= 100 and self.level != self.MANAGER:
            self.level = self.MANAGER
            self.save(update_fields=['level'])

    def __str__(self):
        return f"Profil de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()