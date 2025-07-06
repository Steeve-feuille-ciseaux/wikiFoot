from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('joueurs/', views.liste_joueurs, name='liste_joueurs'),
    path('joueurs/<int:pk>/', views.joueur_detail, name='joueur_detail'),
    path('joueurs/ajouter/', views.ajouter_joueur, name='ajouter_joueur'),
    path('joueurs/modifier/<int:joueur_id>/', views.modifier_joueur, name='modifier_joueur'),
    path('joueur/supprimer/<int:pk>/', views.joueur_supprimer, name='joueur_supprimer'),
    path('', views.home, name=''),
]