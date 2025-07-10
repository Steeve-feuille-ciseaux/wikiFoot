from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Joueur
from .forms import JoueurForm
from .models import Club
from .forms import ClubForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'base.html')

# Onglet Joueurs
def liste_joueurs(request):
    joueurs = Joueur.objects.all()  # récupère tous les joueurs en base
    return render(request, 'joueurs/liste_joueurs.html', {'joueurs': joueurs})

def joueur_detail(request, pk):
    joueur = get_object_or_404(Joueur, pk=pk)
    return render(request, 'joueurs/joueur_detail.html', {'joueur': joueur})

def ajouter_joueur(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_joueurs')  # Modifie selon ton nom de vue de liste
    else:
        form = JoueurForm()

    return render(request, 'joueurs/ajouter_joueur.html', {'form': form})

def modifier_joueur(request, joueur_id):
    joueur = get_object_or_404(Joueur, id=joueur_id)

    if request.method == 'POST':
        form = JoueurForm(request.POST, request.FILES, instance=joueur)
        if form.is_valid():
            form.save()
            return redirect('joueur_detail', joueur.id)
    else:
        form = JoueurForm(instance=joueur)

    return render(request, 'joueurs/modifier_joueur.html', {'form': form, 'joueur': joueur})

def joueur_supprimer(request, pk):
    joueur = get_object_or_404(Joueur, pk=pk)
    
    if request.method == 'POST':
        joueur.delete()
        messages.success(request, "Le joueur a bien été supprimé.")
        return redirect('liste_joueurs')  # Nom de la route de ta liste des joueurs
    
    # Optionnel : afficher une page de confirmation avant suppression
    return render(request, 'joueurs/joueur_confirm_delete.html', {'joueur': joueur})

# Onglet Clubs
def liste_clubs(request):
    clubs = Club.objects.all()  # récupère tous les clubs en base
    return render(request, 'clubs/liste_clubs.html', {'clubs': clubs})

def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    return render(request, 'clubs/club_detail.html', {'club': club})

def ajouter_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le club a bien été ajouté.")
            return redirect('liste_clubs')
    else:
        form = ClubForm()

    return render(request, 'clubs/ajouter_club.html', {'form': form})

def modifier_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, "Le club a bien été modifié.")
            return redirect('club_detail', pk=club.id)
    else:
        form = ClubForm(instance=club)

    return render(request, 'clubs/modifier_club.html', {'form': form, 'club': club})

def club_supprimer(request, pk):
    club = get_object_or_404(Club, pk=pk)

    if request.method == 'POST':
        club.delete()
        messages.success(request, "Le club a bien été supprimé.")
        return redirect('liste_clubs')

    return render(request, 'clubs/club_confirm_delete.html', {'club': club})
