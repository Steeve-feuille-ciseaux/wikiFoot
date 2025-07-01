from django.shortcuts import render, get_object_or_404
from .models import Joueur

def liste_joueurs(request):
    joueurs = Joueur.objects.all()  # récupère tous les joueurs en base
    return render(request, 'joueurs/liste_joueurs.html', {'joueurs': joueurs})

def joueur_detail(request, pk):
    joueur = get_object_or_404(Joueur, pk=pk)
    return render(request, 'joueurs/joueur_detail.html', {'joueur': joueur})
