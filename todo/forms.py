from django import forms
from .models import Membre

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Membre
        # On garde 'sexe' caché juste le temps de la migration
        fields = ['last_name', 'first_name']