from django.db import models

class Continent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    confederation = models.CharField(max_length=100, null=True, blank=True, default='Inconnue')

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    flag = models.ImageField(upload_to='drapeau/')  # ou ImageField si tu gères des images
    culture = models.TextField(max_length=100, null=True, blank=True, default='Inconnue')
    capital = models.CharField(max_length=100, null=True, blank=True, default='Inconnue')

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
    action = models.CharField(max_length=100)
    gif = models.ImageField(upload_to='Gifs/', null=True, blank=True)
    resume = models.TextField()
    statut = models.BooleanField(default=True)
    stade = models.CharField(max_length=100)
    match = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.club.name} - {self.name}"
    
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
    
class NationalTeam(models.Model):
    name = models.CharField(max_length=100)
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='national_team')
    story = models.TextField(null=True, blank=True)
    card_player = models.OneToOneField(Card, on_delete=models.SET_NULL, null=True, blank=True, related_name='national_team_card')
    logo = models.ImageField(upload_to='nationalTeam/', null=True, blank=True)

    def __str__(self):
        return self.name
    
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
