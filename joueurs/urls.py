from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    # Onglet joueurs
    path('joueurs/', views.liste_joueurs, name='liste_joueurs'),
    path('joueurs/<int:pk>/', views.joueur_detail, name='joueur_detail'),
    path('joueurs/ajouter/', views.ajouter_joueur, name='ajouter_joueur'),
    path('joueurs/modifier/<int:joueur_id>/', views.modifier_joueur, name='modifier_joueur'),
    path('joueur/supprimer/<int:pk>/', views.joueur_supprimer, name='joueur_supprimer'),

    # Onglet Clubs
    path('clubs/', views.liste_clubs, name='liste_clubs'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('clubs/ajouter/', views.ajouter_club, name='ajouter_club'),
    path('clubs/modifier/<int:club_id>/', views.modifier_club, name='modifier_club'),
    path('clubs/supprimer/<int:pk>/', views.club_supprimer, name='club_supprimer'),


    path('', views.home, name=''),
]