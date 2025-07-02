from django.urls import path
from . import views

urlpatterns = [
    path('joueurs/', views.liste_joueurs, name='liste_joueurs'),
    path('joueurs/<int:pk>/', views.joueur_detail, name='joueur_detail'),
    path('', views.home, name=''),
]