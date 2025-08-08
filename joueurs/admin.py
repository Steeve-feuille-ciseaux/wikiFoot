from django.contrib import admin

from django.contrib import admin
from .models import (Joueur, Country, Continent, Club, Card, NationalTeam, Competition, CompetitionWin, SelectionTeam,
                      Award, AwardWin, LineUp, Championship, ChampionshipWin, Move, Type, Formation, Style, Entraineur,
                      Profile, Match, City, Stade, Story, Telling)

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
admin.site.register(LineUp)
admin.site.register(Championship)
admin.site.register(ChampionshipWin)
admin.site.register(Move)
admin.site.register(Entraineur)
admin.site.register(Type)
admin.site.register(Style)
admin.site.register(Formation)
admin.site.register(Profile)
admin.site.register(Match)
admin.site.register(City)
admin.site.register(Stade)
admin.site.register(Story)
admin.site.register(Telling)