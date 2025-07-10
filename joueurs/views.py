from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Joueur, Club, Country, Card
from .forms import JoueurForm, ClubForm, CountryForm, CardForm
# from .models import Club
# from .forms import ClubForm
# from .models import Country
# from .forms import CountryForm  

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
    return render(request, 'joueurs/detail_joueur.html', {'joueur': joueur})

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
    return render(request, 'joueurs/confirm_delete_joueur.html', {'joueur': joueur})

# Onglet Clubs
def liste_clubs(request):
    clubs = Club.objects.all()  # récupère tous les clubs en base
    return render(request, 'clubs/liste_clubs.html', {'clubs': clubs})

def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    return render(request, 'clubs/detail_club.html', {'club': club})

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

    return render(request, 'clubs/confirm_delete_club.html', {'club': club})

# Onglet Pays

def liste_pays(request):
    pays = Country.objects.all()  # Récupère tous les pays
    return render(request, 'pays/liste_pays.html', {'pays': pays})

def detail_pays(request, pk):
    pays = get_object_or_404(Country, pk=pk)
    return render(request, 'pays/detail_pays.html', {'pays': pays})

def ajouter_pays(request):
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le pays a bien été ajouté.")
            return redirect('liste_pays')
    else:
        form = CountryForm()

    return render(request, 'pays/ajouter_pays.html', {'form': form})

def modifier_pays(request, pays_id):
    pays = get_object_or_404(Country, id=pays_id)

    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=pays)
        if form.is_valid():
            form.save()
            messages.success(request, "Le pays a bien été modifié.")
            return redirect('detail_pays', pk=pays.id)
    else:
        form = CountryForm(instance=pays)

    return render(request, 'pays/modifier_pays.html', {'form': form, 'pays': pays})

def supprimer_pays(request, pk):
    pays = get_object_or_404(Country, pk=pk)

    if request.method == 'POST':
        pays.delete()
        messages.success(request, "Le pays a bien été supprimé.")
        return redirect('liste_pays')

    return render(request, 'pays/confirm_delete_pays.html', {'pays': pays})

# Onglet Cartes
def liste_cartes(request):
    cartes = Card.objects.all()
    return render(request, 'cards/liste_card.html', {'cartes': cartes})

def carte_detail(request, pk):
    carte = get_object_or_404(Card, pk=pk)
    return render(request, 'cards/detail_card.html', {'carte': carte})

def ajouter_carte(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "La carte a bien été ajoutée.")
            return redirect('liste_card')
    else:
        form = CardForm()
    
    return render(request, 'cards/ajouter_card.html', {'form': form})

def modifier_carte(request, carte_id):
    carte = get_object_or_404(Card, id=carte_id)

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=carte)
        if form.is_valid():
            form.save()
            messages.success(request, "La carte a bien été modifiée.")
            return redirect('detail_carte', pk=carte.id)
    else:
        form = CardForm(instance=carte)

    return render(request, 'cards/modifier_card.html', {'form': form, 'carte': carte})

def supprimer_carte(request, pk):
    carte = get_object_or_404(Card, pk=pk)

    if request.method == 'POST':
        carte.delete()
        messages.success(request, "La carte a bien été supprimée.")
        return redirect('liste_cartes')

    return render(request, 'cards/confirm_delete_card.html', {'carte': carte})