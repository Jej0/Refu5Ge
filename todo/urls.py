from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... tes autres URLs ...
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),

    # URL pour le formulaire de changement de mot de passe
    path('modifier-mot-de-passe/', auth_views.PasswordChangeView.as_view(
        template_name='todo/password_change.html',
        success_url='/profil/modifier/' # Redirection après succès
    ), name='password_change'),

    # URL pour confirmer que c'est fait (optionnel)
    path('modifier-mot-de-passe/succes/', auth_views.PasswordChangeDoneView.as_view(
        template_name='todo/password_change_done.html'
    ), name='password_change_done'),
]