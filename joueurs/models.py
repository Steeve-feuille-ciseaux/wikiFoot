from django.db import models
from django.core.exceptions import ValidationError

class Continent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    confederation = models.CharField(max_length=100, null=True, blank=True, default='Inconnue')
    logo = models.ImageField(upload_to='confederation/', null=True, blank=True) 

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100, null=True, blank=True)
    flag = models.ImageField(upload_to='drapeau/') 
    culture = models.TextField(max_length=100, null=True, blank=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    federation = models.CharField(max_length=100, unique=True, null=True, blank=True)
    logo_federation = models.ImageField(upload_to='federation/', null=True, blank=True)

    def __str__(self):
        return self.name

class Joueur(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    old = models.IntegerField(null=True, blank=True)  # âge / ancienneté ?
    date_of_birth = models.DateField()
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, related_name='joueurs')
    position = models.CharField(max_length=50)
    number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='joueurs/')
    resume = models.TextField(null=True, blank=True)
    # championship_win = models.ForeignKey('ChampionshipWin', on_delete=models.SET_NULL, null=True, blank=True)
    # competition_win = models.ForeignKey('CompetitionWin', on_delete=models.SET_NULL, null=True, blank=True)
    # award = models.ForeignKey('PlayerSuccess', on_delete=models.SET_NULL, null=True, blank=True)
    # club = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True, blank=True)
    # card = models.ForeignKey('Card', on_delete=models.SET_NULL, null=True, blank=True)
    # national_team = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Card(models.Model):
    joueur = models.ForeignKey('Joueur', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards')
    name = models.CharField(max_length=100)
    numero = models.IntegerField()
    position = models.CharField(max_length=100)
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
    national_team = models.ForeignKey('NationalTeam', on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
    img = models.ImageField(upload_to='imgCard/', null=True, blank=True)
    resume = models.TextField()
    statut = models.BooleanField(default=True)
    stade = models.CharField(max_length=100)
    match = models.CharField(max_length=100)
    date = models.DateTimeField()

    # Nouvelles relations vers Move
    move_select1 = models.ForeignKey('Move', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards_select1')
    move_select2 = models.ForeignKey('Move', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards_select2')
    move_select3 = models.ForeignKey('Move', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards_select3')
    move_select4 = models.ForeignKey('Move', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards_select4')
    move_select5 = models.ForeignKey('Move', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards_select5')

    def clean(self):
        super().clean()
        # Vérifie l'exclusivité entre club et national_team
        if (self.club and self.national_team) or (not self.club and not self.national_team):
            raise ValidationError("Soit un club OU une équipe nationale doit être sélectionné(e), mais pas les deux ni aucun.")

        selected_moves = [
            self.move_select1,
            self.move_select2,
            self.move_select3,
            self.move_select4,
            self.move_select5,
        ]

        # Supprime les valeurs nulles
        filtered_moves = [move for move in selected_moves if move is not None]

        if len(filtered_moves) != len(set(filtered_moves)):
            raise ValidationError("Un même Move ne peut pas être sélectionné plusieurs fois.")

    def __str__(self):
        joueur_nom = self.joueur.last_name if self.joueur else 'No Player'
        club_nom = self.club.name if self.club else None
        national_team_nom = self.national_team.name if self.national_team else None

        equipe = club_nom if club_nom else national_team_nom if national_team_nom else 'No Team'

        return f"{joueur_nom} {self.numero} - {equipe} - {self.name}"
    
class Club(models.Model):
    name = models.CharField(max_length=100)
    blazon = models.ImageField(upload_to='club/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='clubs')
    story = models.TextField(unique=True)
    rival = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True)
    # card_player = models.OneToOneField(Card, on_delete=models.SET_NULL, null=True, blank=True, unique=True)
    stade = models.CharField(max_length=100)

    def __str__(self):
        return self.name   
    
class LineUp(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='line_up', null=True, blank=True)
    championship = models.ForeignKey('Championship', on_delete=models.CASCADE, related_name='line_up')
    photo = models.ImageField(upload_to='lineUp/', null=True, blank=True)
    resume = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.club.name} - {self.championship.name} {self.championship.date}"
    
class NationalTeam(models.Model):
    name = models.CharField(max_length=100)
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='national_team')
    story = models.TextField(null=True, blank=True)
    card_player = models.OneToOneField(Card, on_delete=models.SET_NULL, null=True, blank=True, related_name='national_team_card')
    logo = models.ImageField(upload_to='nationalTeam/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Championship(models.Model):
    name = models.CharField(max_length=100)  # correspond à id_name    
    date = models.PositiveIntegerField(default=1998)
    logo = models.ImageField(upload_to='championship/', null=True, blank=True)  
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='championships')
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True, blank=True, related_name='championships')

    def __str__(self):
        return f"{self.name} {self.date}"
    
class ChampionshipWin(models.Model):
    player = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='championship_wins')
    championship = models.ForeignKey('Championship', on_delete=models.CASCADE, related_name='wins')
    line_up = models.OneToOneField('LineUp', on_delete=models.SET_NULL, null=True, blank=True, related_name='championship_win')
    date = models.PositiveIntegerField(default=2016)
    old = models.IntegerField()  # âge du joueur au moment de la victoire
    # team = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='competition_wins')

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} - {self.championship.name} ({self.date})"
    
class Competition(models.Model):
    name = models.CharField(max_length=100)  # correspond à id_name    
    date = models.PositiveIntegerField(default=1998)
    logo = models.ImageField(upload_to='competition/', null=True, blank=True)  # tu avais "logo integer", j'imagine une image
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='competitions')
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True, blank=True, related_name='competitions')

    def __str__(self):
        return f"{self.name} {self.date}"
    
class CompetitionWin(models.Model):
    player = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='competition_wins')
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='wins')
    selection_team = models.OneToOneField('SelectionTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='competition_win')
    date = models.PositiveIntegerField(default=2016)
    old = models.IntegerField()  # âge du joueur au moment de la victoire
    # team = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='competition_wins')

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} - {self.competition.name} ({self.date})"
    
class SelectionTeam(models.Model):
    team = models.ForeignKey('NationalTeam', on_delete=models.CASCADE, related_name='selection_teams', null=True, blank=True)
    selection_competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='selection_teams')
    photo = models.ImageField(upload_to='selectionTeam/', null=True, blank=True)
    resume = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.team} - {self.selection_competition}"

class Award(models.Model):
    name = models.CharField(max_length=100)  # correspond à id_name
    award = models.ImageField(upload_to='award/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='awards')
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True, blank=True, related_name='awards')

    def __str__(self):
        return self.name

class AwardWin(models.Model):
    player = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='award_wins')
    award = models.ForeignKey('Award', on_delete=models.SET_NULL, null=True, blank=True, related_name='wins')
    date = models.PositiveIntegerField(default=1998)
    old = models.IntegerField(null=True, blank=True)  # âge du joueur au moment de la récompense

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} - {self.award.name if self.award else 'N/A'} {self.date}"

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Move(models.Model):
    name = models.CharField(max_length=100)
    resume = models.TextField()
    minute = models.IntegerField()
    gif = models.ImageField(upload_to='Gifs/', null=True, blank=True)
    typeMove  = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='moves')

    def __str__(self):
        return f"{self.name} - {self.typeMove}"
    
class Entraineur(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    old = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField()
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, related_name='entraineurs')
    image = models.ImageField(upload_to='entraineurs/', null=True, blank=True)
    style = models.TextField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)
    # championship_win = models.ForeignKey('ChampionshipWin', on_delete=models.SET_NULL, null=True, blank=True)
    # competition_win = models.ForeignKey('CompetitionWin', on_delete=models.SET_NULL, null=True, blank=True)
    # award = models.ForeignKey('PlayerSuccess', on_delete=models.SET_NULL, null=True, blank=True)
    # club = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True, blank=True)
    # card = models.ForeignKey('Card', on_delete=models.SET_NULL, null=True, blank=True)
    # national_team = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"