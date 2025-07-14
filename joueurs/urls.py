from django.urls import path
from . import views
from .views import register, liste_utilisateurs
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import CustomPasswordChangeView

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('utilisateurs/modifier/', views.edit_profile, name='edit_profile'),
    path('changer-mot-de-passe/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('utilisateur/', views.profile_view, name='profile'),

    # Onglet Management user
    path('utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateur/<int:pk>/', views.utilisateur_detail, name='utilisateur_detail'),
    path('utilisateur/<int:pk>/edit/', views.utilisateur_edit, name='utilisateur_edit'),
    path('utilisateur/<int:pk>/delete/', views.utilisateur_delete, name='utilisateur_delete'),

    # Feature Recherche
    path('recherche/', views.recherche, name='recherche'),
    
    # Onglet Entraîneur
    path('entraineurs/', views.liste_entraineurs, name='liste_entraineurs'),
    path('entraineurs/<int:pk>/', views.entraineur_detail, name='entraineur_detail'),
    path('entraineurs/ajouter/', views.ajouter_entraineur, name='ajouter_entraineur'),
    path('entraineurs/modifier/<int:entraineur_id>/', views.modifier_entraineur, name='modifier_entraineur'),
    path('entraineurs/supprimer/<int:pk>/', views.supprimer_entraineur, name='supprimer_entraineur'),
    path('entraineurs/en-attente/', views.waiting_entraineurs, name='waiting_entraineurs'),

    # Onglet joueurs
    path('joueurs/', views.liste_joueurs, name='liste_joueurs'),
    path('joueurs/<int:pk>/', views.joueur_detail, name='joueur_detail'),
    path('joueurs/ajouter/', views.ajouter_joueur, name='ajouter_joueur'),
    path('joueurs/modifier/<int:joueur_id>/', views.modifier_joueur, name='modifier_joueur'),
    path('joueur/supprimer/<int:pk>/', views.joueur_supprimer, name='joueur_supprimer'),
    path('joueurs/en-attente/', views.waiting_joueurs, name='waiting_joueurs'),

    # Onglet Clubs
    path('clubs/', views.liste_clubs, name='liste_clubs'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('clubs/ajouter/', views.ajouter_club, name='ajouter_club'),
    path('clubs/modifier/<int:club_id>/', views.modifier_club, name='modifier_club'),
    path('clubs/supprimer/<int:pk>/', views.club_supprimer, name='club_supprimer'),
    path('clubs/en-attente/', views.waiting_clubs, name='waiting_clubs'),

    # Onglet Pays
    path('pays/', views.liste_pays, name='liste_pays'),
    path('pays/<int:pk>/', views.detail_pays, name='detail_pays'),
    path('pays/ajouter/', views.ajouter_pays, name='ajouter_pays'),
    path('pays/<int:pays_id>/modifier/', views.modifier_pays, name='modifier_pays'),
    path('pays/<int:pk>/supprimer/', views.supprimer_pays, name='supprimer_pays'),
    path('pays/en-attente/', views.waiting_pays, name='waiting_pays'),

    # Onglet Cards
    path('cartes/', views.liste_cartes, name='liste_carte'),
    path('cartes/<int:pk>/', views.carte_detail, name='detail_carte'),
    path('cartes/ajouter/', views.ajouter_carte, name='ajouter_carte'),
    path('cartes/modifier/<int:carte_id>/', views.modifier_carte, name='modifier_carte'),
    path('cartes/supprimer/<int:pk>/', views.supprimer_carte, name='supprimer_carte'),
    path('cartes/en-attente/', views.waiting_cartes, name='waiting_cartes'),

    # Onglet Move
    path('moves/', views.liste_moves, name='liste_moves'),
    path('moves/<int:pk>/', views.move_detail, name='move_detail'),
    path('moves/ajouter/', views.ajouter_move, name='ajouter_move'),
    path('moves/modifier/<int:move_id>/', views.modifier_move, name='modifier_move'),
    path('moves/supprimer/<int:pk>/', views.supprimer_move, name='supprimer_move'),
    path('moves/en-attente/', views.waiting_moves, name='waiting_moves'),

    path('', views.home, name=''),
]