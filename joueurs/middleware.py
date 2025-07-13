from .models import Entraineur

class VisibleCoachesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ajouter le nombre d'entraîneurs visibles (visible=False) à la requête
        request.visible_coaches_count = Entraineur.objects.filter(visible=False).count()
        
        # Récupérer la réponse à partir de la fonction get_response
        response = self.get_response(request)

        # Ajoute la variable à chaque réponse, dans le contexte
        if hasattr(response, 'context_data'):
            response.context_data['visible_coaches_count'] = request.visible_coaches_count

        return response
