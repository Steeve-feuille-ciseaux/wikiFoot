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
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='cards')
    action = models.CharField(max_length=100)
    gif = models.ImageField(upload_to='Gifs/', null=True, blank=True)
    resume = models.TextField()
    statut = models.BooleanField(default=True)
    stade = models.CharField(max_length=100)
    match = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.club.name} - {self.action}"
    
class Club(models.Model):
    name = models.CharField(max_length=100)
    blazon = models.ImageField(upload_to='Blazon/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='clubs')
    story = models.TextField(unique=True)
    rival = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True)
    # card_player = models.OneToOneField(Card, on_delete=models.SET_NULL, null=True, blank=True, unique=True)
    stade = models.CharField(max_length=100)

    def __str__(self):
        return self.name