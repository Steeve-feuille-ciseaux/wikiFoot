# joueurs/forms.py
from django import forms
from .models import Joueur, Club

class JoueurForm(forms.ModelForm):
    class Meta:
        model = Joueur
        fields = '__all__'
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'club': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'blazon': forms.FileInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'story': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rival': forms.Select(attrs={'class': 'form-control'}),
            'stade': forms.TextInput(attrs={'class': 'form-control'}),
        }
