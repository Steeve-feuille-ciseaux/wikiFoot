from django.contrib import admin

from django.contrib import admin
from .models import Joueur, Country, Continent

admin.site.register(Joueur)
admin.site.register(Country)
admin.site.register(Continent)