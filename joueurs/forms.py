# joueurs/forms.py
from django import forms
from .models import Joueur, Club, Country, Card

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
        
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'continent': forms.Select(attrs={'class': 'form-control'}),
            'flag': forms.FileInput(attrs={'class': 'form-control'}),
            'culture': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capital': forms.TextInput(attrs={'class': 'form-control'}),
            'federation': forms.TextInput(attrs={'class': 'form-control'}),
            'logo_federation': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        widgets = {
            'joueur': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'club': forms.Select(attrs={'class': 'form-control'}),
            'national_team': forms.Select(attrs={'class': 'form-control'}),
            'img': forms.FileInput(attrs={'class': 'form-control'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'statut': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stade': forms.TextInput(attrs={'class': 'form-control'}),
            'match': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),

            # Move selections
            'move_select1': forms.Select(attrs={'class': 'form-control'}),
            'move_select2': forms.Select(attrs={'class': 'form-control'}),
            'move_select3': forms.Select(attrs={'class': 'form-control'}),
            'move_select4': forms.Select(attrs={'class': 'form-control'}),
            'move_select5': forms.Select(attrs={'class': 'form-control'}),
        }