from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.accueil, name='home'),             # Accueil 
    path('recherche/', views.recherche, name='recherche'),  # Recherche publique
]
