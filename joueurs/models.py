from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Continent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    confederation = models.CharField(max_length=100, null=True, blank=True, default='Inconnue')
    logo = models.ImageField(upload_to='confederation/', null=True, blank=True) 

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capital = models.OneToOneField('City', on_delete=models.SET_NULL, null=True, blank=True, related_name='country_capital')
    flag = models.ImageField(upload_to='drapeau/') 
    culture = models.TextField(max_length=100, null=True, blank=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    federation = models.CharField(max_length=100, unique=True, null=True, blank=True)
    logo_federation = models.ImageField(upload_to='federation/', null=True, blank=True)
    visible = models.BooleanField(default=False)
    storytelling = models.OneToOneField('Story', on_delete=models.SET_NULL, null=True, blank=True)

    # Suivi
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='pays_created')
    updated_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='pays_updated')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name_country')
        ]

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
    visible = models.BooleanField(default=False)    
    storytelling = models.OneToOneField('Story', on_delete=models.SET_NULL, null=True, blank=True)

    # Suivi
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='joueurs_created')
    updated_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='joueurs_updated')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'], name='unique_full_name_joueur')
        ]

class Card(models.Model):
    joueur = models.ForeignKey('Joueur', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards')
    name = models.CharField(max_length=100)
    numero = models.IntegerField()
    position = models.CharField(max_length=100)
    club = models.ForeignKey('Club', on_delete=models.CASCADE, null=True, blank=True, related_name='card_clubs')
    national_team = models.ForeignKey('NationalTeam', on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
    img = models.ImageField(upload_to='imgCard/', null=True, blank=True)
    resume = models.TextField()
    statut = models.BooleanField(default=True)
    stade = models.CharField(max_length=100, null=True, blank=True)
    match = models.ForeignKey('Match', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField()
    visible = models.BooleanField(default=False)

    # Suivi
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards_created')
    updated_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='cards_updated')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name_cards')
        ]
    
class Club(models.Model):
    name = models.CharField(max_length=100)
    blazon = models.ImageField(upload_to='club/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='clubs')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs') 
    story = models.TextField(unique=True)
    rival = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True)
    stade = models.ForeignKey('Stade', on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs_stadium')
    visible = models.BooleanField(default=False)
    storytelling = models.OneToOneField('Story', on_delete=models.SET_NULL, null=True, blank=True)

    # Suivi
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs_created')
    updated_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs_updated')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name_club')
        ]
    
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
    player = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='championship_wins', null=True, blank=True)
    coach = models.ForeignKey('Entraineur', on_delete=models.CASCADE, related_name='championship_wins', null=True, blank=True)
    championship = models.ForeignKey('Championship', on_delete=models.CASCADE, related_name='wins')
    line_up = models.OneToOneField('LineUp', on_delete=models.SET_NULL, null=True, blank=True, related_name='championship_win')
    date = models.PositiveIntegerField(default=2016)
    old = models.IntegerField()  # âge du joueur au moment de la victoire
    # team = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='competition_wins')

    def __str__(self):
        return f"{self.player or self.coach} - {self.championship.name} ({self.date})"

    def clean(self):
        if not self.player and not self.coach:
            raise ValidationError("Un gagnant doit être soit un joueur, soit un entraîneur.")
    
class Competition(models.Model):
    name = models.CharField(max_length=100)  # correspond à id_name    
    date = models.PositiveIntegerField(default=1998)
    logo = models.ImageField(upload_to='competition/', null=True, blank=True)  # tu avais "logo integer", j'imagine une image
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='competitions')
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True, blank=True, related_name='competitions')

    def __str__(self):
        return f"{self.name} {self.date}"
    
class CompetitionWin(models.Model):
    player = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='competition_wins', null=True, blank=True)
    coach = models.ForeignKey('Entraineur', on_delete=models.CASCADE, related_name='competition_wins', null=True, blank=True)
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='wins')
    selection_team = models.OneToOneField('SelectionTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='competition_win')
    date = models.PositiveIntegerField(default=2016)
    old = models.IntegerField()  # âge du joueur au moment de la victoire
    # team = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='competition_wins')

    def __str__(self):
        return f"{self.player or self.coach} - {self.competition.name} ({self.date})"

    def clean(self):
        # Vérifie qu'au moins l'un des deux (player ou coach) est renseigné
        if not self.player and not self.coach:
            raise ValidationError("Un vainqueur doit être soit un joueur, soit un entraîneur.")
    
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
    player = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='award_wins', null=True, blank=True)
    coach = models.ForeignKey('Entraineur', on_delete=models.CASCADE, related_name='award_wins', null=True, blank=True)
    award = models.ForeignKey('Award', on_delete=models.SET_NULL, null=True, blank=True, related_name='wins')
    date = models.PositiveIntegerField(default=1998)
    old = models.IntegerField(null=True, blank=True)  # âge du joueur au moment de la récompense

    def __str__(self):
        return f"{self.player or self.coach} - {self.award.name if self.award else 'N/A'} {self.date}"

    def clean(self):
        if not self.player and not self.coach:
            raise ValidationError("Un gagnant doit être soit un joueur, soit un entraîneur.")

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
    visible = models.BooleanField(default=False)

    # Suivi
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='moves_created')
    updated_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='moves_updated')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.typeMove}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name_moves')
        ]
    
class Entraineur(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    old = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField()
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, related_name='entraineurs')
    image = models.ImageField(upload_to='entraineurs/', null=True, blank=True)
    style = models.ForeignKey('Style', on_delete=models.SET_NULL, null=True, blank=True, related_name='entraineurs')
    formation = models.ForeignKey('Formation', on_delete=models.SET_NULL, null=True, blank=True, related_name='entraineurs')
    resume = models.TextField(null=True, blank=True)
    career_player = models.OneToOneField('Joueur', on_delete=models.SET_NULL, null=True, blank=True, related_name='entraineur_carriere')
    visible = models.BooleanField(default=False)
    storytelling = models.OneToOneField('Story', on_delete=models.SET_NULL, null=True, blank=True)

    # Suivi
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='entraineurs_created')
    updated_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='entraineurs_updated')
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    # championship_win = models.ForeignKey('ChampionshipWin', on_delete=models.SET_NULL, null=True, blank=True)
    # competition_win = models.ForeignKey('CompetitionWin', on_delete=models.SET_NULL, null=True, blank=True)
    # award = models.ForeignKey('PlayerSuccess', on_delete=models.SET_NULL, null=True, blank=True)
    # club = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True, blank=True)
    # card = models.ForeignKey('Card', on_delete=models.SET_NULL, null=True, blank=True)
    # national_team = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'], name='unique_full_name_entraineur')
        ]

class Style(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Formation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('moderator', 'Modérateur'),
        ('creator', 'Créateur'),
        ('user', 'Utilisateur'),
    ]

    RANK_BY_ROLE = {
        'admin': 4,
        'moderator': 3,
        'creator': 2,
        'user': 1,
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    rank = models.IntegerField(editable=False)  # auto-set, pas modifiable depuis l’admin

    def save(self, *args, **kwargs):
        self.rank = self.RANK_BY_ROLE.get(self.role, 1)  # Définit automatiquement le rang
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()} (Rang {self.rank})"
    
    
class Match(models.Model):
    name = models.CharField(max_length=100)  # Ex: "Finale Coupe du Monde 2018"
    date = models.DateTimeField()

    # Participants (clubs OU équipes nationales)
    club1 = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='home_matches')
    club2 = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='away_matches')
    national_team1 = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='home_national_matches')
    national_team2 = models.ForeignKey('NationalTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='away_national_matches')

    # Score
    score_team1 = models.IntegerField(null=True, blank=True)
    score_team2 = models.IntegerField(null=True, blank=True)

    # Contexte
    competition = models.ForeignKey('Competition', on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    context = models.TextField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        team1 = self.club1.name if self.club1 else self.national_team1.name if self.national_team1 else "Équipe 1"
        team2 = self.club2.name if self.club2 else self.national_team2.name if self.national_team2 else "Équipe 2"
        return f"{team1} vs {team2} - {self.name}"

    def clean(self):
        # Un match doit opposer deux clubs OU deux nations, pas un mix
        is_club_match = self.club1 or self.club2
        is_national_match = self.national_team1 or self.national_team2

        if is_club_match and is_national_match:
            raise ValidationError("Un match doit être entre deux clubs OU deux équipes nationales, pas les deux.")
        
        if (self.club1 and not self.club2) or (self.club2 and not self.club1):
            raise ValidationError("Les deux clubs doivent être renseignés pour un match de club.")
        
        if (self.national_team1 and not self.national_team2) or (self.national_team2 and not self.national_team1):
            raise ValidationError("Les deux équipes nationales doivent être renseignées pour un match international.")
        
        if not (self.club1 and self.club2) and not (self.national_team1 and self.national_team2):
            raise ValidationError("Un match doit avoir deux clubs OU deux équipes nationales.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'date'], name='unique_match_name_date')
        ]

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='cities')
    culture = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.country.name if self.country else 'Sans pays'})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='unique_city_per_country')
        ]

class Stade(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='stades')  # 🔄 remplace location
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='stades')  # 🔄 ajout
    capacity = models.IntegerField(null=True, blank=True)
    histoire = models.TextField(null=True, blank=True)  # 🔄 ajout
    club = models.OneToOneField('Club', on_delete=models.SET_NULL, null=True, blank=True, related_name='stadium_owned')

    def clean(self):
        if not self.club:
            raise ValidationError("Un stade doit appartenir à un club.")

    def __str__(self):
        return self.name
    
class Story(models.Model):
    name = models.CharField(max_length=255)
    intro = models.TextField()

    def __str__(self):
        return self.name

class Telling(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tellings')
    text_telling = models.TextField()
    img_telling = models.ImageField(upload_to='story/', null=True, blank=True)

    def __str__(self):
        tellings = list(self.story.tellings.order_by('id'))
        index = tellings.index(self) + 1  # position de ce telling
        last_index = len(tellings)  # total des tellings pour cette story
        return f"{index} / {last_index} - {self.story.name}"