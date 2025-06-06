from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User, Annonce, Categorie


class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'numeroTelephone', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.image = ""
            user.save()
        return user

class BaseProfileForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['image', 'nom', 'prenom', 'email', 'numeroTelephone']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'numeroTelephone': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control','style': 'display:none;'}),
        }


class ModifierAnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'prix', 'statut', 'categorie', 'isPremieum']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
        labels = {
            'isPremieum': 'Annonce Premium'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorie'].queryset = Categorie.objects.all().order_by('nom')

