from django.contrib import admin

from django.contrib import admin
from .models import Joueur, Country, Continent, Club, Card

admin.site.register(Joueur)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(Club)
admin.site.register(Card)