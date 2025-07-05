from django.contrib import admin

from django.contrib import admin
from .models import Joueur, Country, Continent, Club, Card, NationalTeam, Competition, CompetitionWin, SelectionTeam, Award, AwardWin

admin.site.register(Joueur)
admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(Club)
admin.site.register(Card)
admin.site.register(NationalTeam)
admin.site.register(Competition)
admin.site.register(CompetitionWin)
admin.site.register(SelectionTeam)
admin.site.register(Award)
admin.site.register(AwardWin)