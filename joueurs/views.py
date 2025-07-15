from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Joueur, Club, Country, Card, Move, Entraineur
from .forms import JoueurForm, ClubForm, CountryForm, CardForm, MoveForm, EntraineurForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

@login_required
def dashboard(request):
    return render(request, 'base.html')

@login_required
def utilisateur_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'registration/utilisateur_detail.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.profile.rank == 4)
def liste_utilisateurs(request):
    utilisateurs = User.objects.select_related('profile').all().order_by('username')
    return render(request, 'registration/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

@login_required
@user_passes_test(lambda u: u.profile.rank == 4)
def utilisateur_edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur modifié avec succès.")
            return redirect('utilisateur_detail', pk=user.pk)
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'registration/edit_utilisateur.html', {'form': form, 'user': user})

@login_required
@user_passes_test(lambda u: u.profile.rank == 4)
def utilisateur_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Empêche la suppression de soi-même
    if request.user == user:
        messages.error(request, "Vous ne pouvez pas vous supprimer vous-même.")
        return redirect('liste_utilisateurs')

    if request.method == 'POST':
        user.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect('liste_utilisateurs')

    return render(request, 'registration/confirm_delete_utilisateur.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'registration/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    profile = user.profile  # via OneToOneField

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'registration/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Mot de passe changé avec succès.")
            # return redirect('login')  # ou la page que tu souhaites
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'registration/change_password.html', {'password_form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Mot de passe changé avec succès.")
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Création d'un profil par défaut
            Profile.objects.create(
                user=user,
                role='utilisateur',  # ou "Utilisateur" selon ta logique
                rank=1
            )

            messages.success(request, "Compte créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'base.html')

# Feature Rechercher
def recherche(request):
    query = request.GET.get('search', '')
    joueurs = []
    entraineurs = []

    if query:
        joueurs = Joueur.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        entraineurs = Entraineur.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )

    return render(request, 'recherche_resultats.html', {
        'query': query,
        'joueurs': joueurs,
        'entraineurs': entraineurs,
    })

# Onglet Joueurs
def liste_joueurs(request):
    joueurs = Joueur.objects.filter(visible=True)
    return render(request, 'joueurs/liste_joueurs.html', {'joueurs': joueurs})

def waiting_joueurs(request):
    joueurs_visibles = Joueur.objects.filter(visible=False)
    return render(request, 'joueurs/waiting_joueurs.html', {'joueurs': joueurs_visibles})

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

def valider_joueur(request, pk):
    joueur = get_object_or_404(Joueur, pk=pk)
    joueur.visible = True
    joueur.save()
    messages.success(request, "Le joueur a été validé avec succès.")

    return redirect('liste_joueurs')

# Onglet Clubs
def liste_clubs(request):
    clubs = Club.objects.filter(visible=True)
    return render(request, 'clubs/liste_clubs.html', {'clubs': clubs})

def waiting_clubs(request):
    clubs_visibles = Club.objects.filter(visible=False)
    return render(request, 'clubs/waiting_clubs.html', {'clubs': clubs_visibles})

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

def valider_club(request, pk):
    club = get_object_or_404(Club, pk=pk)
    club.visible = True
    club.save()
    messages.success(request, "Le club a été validé avec succès.")

    return redirect('liste_clubs')

# Onglet Pays
def liste_pays(request):
    pays = Country.objects.filter(visible=True)
    return render(request, 'pays/liste_pays.html', {'pays': pays})

def waiting_pays(request):
    pays_visibles = Country.objects.filter(visible=False)
    return render(request, 'pays/waiting_pays.html', {'pays': pays_visibles})

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

def valider_pays(request, pk):
    pays = get_object_or_404(Country, pk=pk)
    pays.visible = True
    pays.save()
    messages.success(request, "Le pays a été validé avec succès.")

    return redirect('liste_pays')

# Onglet Cartes
def liste_cartes(request):
    cartes = Card.objects.filter(visible=True)
    return render(request, 'cards/liste_card.html', {'cartes': cartes})

def waiting_cartes(request):
    cartes_visibles = Card.objects.filter(visible=False)
    return render(request, 'cards/waiting_cards.html', {'cartes': cartes_visibles})

def carte_detail(request, pk):
    carte = get_object_or_404(Card, pk=pk)
    return render(request, 'cards/detail_card.html', {'carte': carte})

def ajouter_carte(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "La carte a bien été ajoutée.")
            return redirect('liste_carte')
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
        return redirect('liste_carte')

    return render(request, 'cards/confirm_delete_card.html', {'carte': carte})

def valider_carte(request, pk):
    carte = get_object_or_404(Card, pk=pk)
    carte.visible = True
    carte.save()
    messages.success(request, "La carte a été validée avec succès.")

    return redirect('liste_carte')

# Onglet Moves
def liste_moves(request):
    moves = Move.objects.filter(visible=True)
    return render(request, 'moves/liste_move.html', {'moves': moves})

def waiting_moves(request):
    moves_visibles = Move.objects.filter(visible=False)
    return render(request, 'moves/waiting_moves.html', {'moves': moves_visibles})

def move_detail(request, pk):
    move = get_object_or_404(Move, pk=pk)
    return render(request, 'moves/detail_move.html', {'move': move})

def ajouter_move(request):
    if request.method == 'POST':
        form = MoveForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "L'action a bien été ajoutée.")
            return redirect('liste_moves')
    else:
        form = MoveForm()
    
    return render(request, 'moves/ajouter_move.html', {'form': form})

def modifier_move(request, move_id):
    move = get_object_or_404(Move, id=move_id)

    if request.method == 'POST':
        form = MoveForm(request.POST, request.FILES, instance=move)
        if form.is_valid():
            form.save()
            messages.success(request, "L'action a bien été modifiée.")
            return redirect('move_detail', pk=move.id)
    else:
        form = MoveForm(instance=move)

    return render(request, 'moves/modifier_move.html', {'form': form, 'move': move})

def supprimer_move(request, pk):
    move = get_object_or_404(Move, pk=pk)

    if request.method == 'POST':
        move.delete()
        messages.success(request, "L'action a bien été supprimée.")
        return redirect('liste_moves')

    return render(request, 'moves/confirm_delete_move.html', {'move': move})

def valider_move(request, pk):
    move = get_object_or_404(Move, pk=pk)
    move.visible = True
    move.save()
    messages.success(request, "L'action a été validée avec succès.")
    return redirect('liste_moves')

# Onglet Entraineurs
def liste_entraineurs(request):
    entraineurs = Entraineur.objects.filter(visible=True)
    return render(request, 'entraineurs/liste_entraineurs.html', {'entraineurs': entraineurs})

def waiting_entraineurs(request):
    entraineurs_visibles = Entraineur.objects.filter(visible=False)
    return render(request, 'entraineurs/waiting_entraineurs.html', {'entraineurs': entraineurs_visibles})

def entraineur_detail(request, pk):
    entraineur = get_object_or_404(Entraineur, pk=pk)
    return render(request, 'entraineurs/detail_entraineur.html', {'entraineur': entraineur})

def ajouter_entraineur(request):
    if request.method == 'POST':
        form = EntraineurForm(request.POST, request.FILES)
        if form.is_valid():
            entraineur = form.save(commit=False)

            # On récupère le profil de l'utilisateur connecté
            if hasattr(request.user, 'profile'):
                entraineur.created_by = request.user.profile
                entraineur.updated_by = request.user.profile  # peut être le même à la création

            entraineur.save()
            messages.success(request, "L'entraîneur a bien été ajouté.")
            return redirect('liste_entraineurs')
    else:
        form = EntraineurForm()

    return render(request, 'entraineurs/ajouter_entraineur.html', {'form': form})

def modifier_entraineur(request, entraineur_id):
    entraineur = get_object_or_404(Entraineur, id=entraineur_id)

    if request.method == 'POST':
        form = EntraineurForm(request.POST, request.FILES, instance=entraineur)
        if form.is_valid():
            entraineur = form.save(commit=False)

            if hasattr(request.user, 'profile'):
                entraineur.updated_by = request.user.profile

            entraineur.save()
            messages.success(request, "L'entraîneur a bien été modifié.")
            return redirect('entraineur_detail', pk=entraineur.id)
    else:
        form = EntraineurForm(instance=entraineur)

    return render(request, 'entraineurs/modifier_entraineur.html', {'form': form, 'entraineur': entraineur})

def supprimer_entraineur(request, pk):
    entraineur = get_object_or_404(Entraineur, pk=pk)

    if request.method == 'POST':
        entraineur.delete()
        messages.success(request, "L'entraîneur a bien été supprimé.")
        return redirect('liste_entraineurs')

    return render(request, 'entraineurs/confirm_delete_entraineur.html', {'entraineur': entraineur})

def valider_entraineur(request, pk):
    
    entraineur = get_object_or_404(Entraineur, pk=pk)
    entraineur.visible = True
    entraineur.save()
    messages.success(request, "L'entraîneur a été validé avec succès.")

    return redirect('liste_entraineurs')