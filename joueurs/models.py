from django.db import models

class Joueur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    position = models.CharField(max_length=50)
    numero = models.IntegerField()
    club = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    image = models.ImageField(upload_to='joueurs/')
    resume = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
