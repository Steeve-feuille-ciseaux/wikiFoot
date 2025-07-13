from .models import Entraineur
from .models import Joueur
from .models import Club
from .models import Card
from .models import Country
from .models import Move

def visible_coaches_count(request):
    # Récupérer le nombre d'entraîneurs avec visible=False
    return {
        'visible_coaches_count': Entraineur.objects.filter(visible=False).count()
    }

def visible_joueurs_count(request):
    # Retourner le nombre de joueurs dont la visibilité est à False
    return {
        'visible_joueurs_count': Joueur.objects.filter(visible=False).count()
    }

def visible_clubs_count(request):
    # Retourner le nombre de clubs dont la visibilité est à False
    return {
        'visible_clubs_count': Club.objects.filter(visible=False).count()
    }

def visible_cards_count(request):
    # Retourner le nombre de cartes dont la visibilité est à False
    return {
        'visible_cards_count': Card.objects.filter(visible=False).count()
    }

def visible_countries_count(request):
    # Retourner le nombre de pays dont la visibilité est à False
    return {
        'visible_countries_count': Country.objects.filter(visible=False).count()
    }

def visible_moves_count(request):
    # Retourner le nombre de mouvements dont la visibilité est à False
    return {
        'visible_moves_count': Move.objects.filter(visible=False).count()
    }