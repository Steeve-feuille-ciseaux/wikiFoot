from .models import Entraineur

def visible_coaches_count(request):
    # Récupérer le nombre d'entraîneurs avec visible=False
    return {
        'visible_coaches_count': Entraineur.objects.filter(visible=False).count()
    }
