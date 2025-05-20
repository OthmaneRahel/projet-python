
import os
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from .forms import InscriptionForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Administrateur, User, Message,Categorie
from .forms import BaseProfileForm, InscriptionForm, BaseProfileFormAdmin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
# def home(request):
#  return render(request, 'base.html')

def inscription(request):
    
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription réussie! Vous pouvez maintenant vous connecter.')
            return redirect('login_page')
        else:
         print(form.errors) 
    else:
        
        form = InscriptionForm()
        
    return render(request, 'Utilisateur/inscription.html', {'form': form})

class LoginPage(View):
   def get(self, request):
    # if 'adm' in request.path:
    #     return render(request, 'Administrateur/loginPage.html')
    return render(request, 'Utilisateur/login.html')

class AuthUtilisateur(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            categories = Categorie.objects.all()
            annonces = Annonce.objects.all().order_by('-datePublication')[:6]  # Récupère les 6 dernières annonces
            return render(request, 'Utilisateur/homePage.html',{'annonces': annonces, 'MEDIA_URL': settings.MEDIA_URL,"categories":categories})  # Redirection après succès
        else:
            messages.error(request, 'Email ou mot de passe invalide.')
            return redirect('login_page')  # On retourne à la page de connexion

    def get(self, request):
        if request.user.is_authenticated:
            categories = Categorie.objects.all()
            annonces = Annonce.objects.all().order_by('-datePublication')[:6]  # Récupère les 6 dernières annonces
            return render(request, 'Utilisateur/homePage.html',{'annonces': annonces, 'MEDIA_URL': settings.MEDIA_URL,"categories":categories})  # Redirection après succès
        return redirect('home')

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('home')
            # return render(request, 'base.html', {'message': 'Vous avez été déconnecté avec succès.'})
        return render(request, 'Utilisateur/homePage.html')
        
def Profil_User(request, user_id):
    return render(request, 'Utilisateur/Profil_User.html', {
        'user': get_object_or_404(User, id=user_id),
        'user_ads': Annonce.objects.filter(user_id = request.user.id),
        'user_ads_count': Annonce.objects.filter(user_id = request.user.id).count(),
        'categories' : Categorie.objects.all(),
        # 'user_favorites_count': fa.objects.filter(user_id = request.user.id).count(),
        'MEDIA_URL':settings.MEDIA_URL
    })

def Profil_modifier(request ):
    if request.method == 'POST':
        form = BaseProfileForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('Profil_User',user_id=request.user.id)
        else:
            print(form.errors)
    else:
        form = BaseProfileForm(instance=request.user)
    return render(request, 'Utilisateur/Modifier_Profil.html', {'form': form})   

from django.http import JsonResponse
from .models import Annonce
import json
from django.core.files.storage import default_storage


from django.core.mail import send_mail
from django.conf import settings

def ajouter_annonce(request):
    if request.method == 'POST':
        
        # Récupération des données du formulaire
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        categorie = request.POST.get('categorie_id')
        prix = float(request.POST.get('prix'))
        is_premieum = request.POST.get('isPremieum') == 'on'
        
        # Gestion des images
        noms_images = []
        images = request.FILES.getlist('images')
        for image in images:
            path = os.path.join('annonces', image.name)
            saved_path = default_storage.save(path, image)
            noms_images.append(saved_path)
        
        # Création de l'annonce avec statut 'en_attente'
        annonce = Annonce.objects.create(
            titre=titre,
            description=description,
            prix=prix,
            user=request.user,
            categorie_id=categorie,
            isPremieum=is_premieum,
            statut='en_attente',  # Statut initial
            images=noms_images
        )

        messages.success(request,'Votre annonce a été soumise pour validation par un administrateur')
        
        return redirect('home_user')

from .forms import ModifierAnnonceForm

def modifier_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    
    if request.method == 'POST':
        form = ModifierAnnonceForm(request.POST, instance=annonce)
        if form.is_valid():
            form.save()
            messages.success(request, "L'annonce a été mise à jour avec succès!")
            return redirect('mes_annonces')
        else:
            print("Erreurs du formulaire:", form.errors)

    else:
        form = ModifierAnnonceForm(instance=annonce)
    
    return render(request, 'Utilisateur/Modifier_Anc.html', {'form': form,'annonce': annonce})

def afficher_annonce_categorie(request,categorie_id):

    annonces = Annonce.objects.filter(categorie_id=categorie_id)
    return render(request, 'Utilisateur/test.html', {
        'annonces': annonces,
        'MEDIA_URL': settings.MEDIA_URL
})

def mes_annonces(request):
    annonces = Annonce.objects.filter(user=request.user).order_by('-datePublication')
    categories = Categorie.objects.all()
    return render(request, 'Utilisateur/Mes_annonces.html', {'annonces': annonces,'MEDIA_URL': settings.MEDIA_URL,'categories': categories})

from .models import Annonce

def home(request):
    categories = Categorie.objects.all()
    annonces = Annonce.objects.all().order_by('-datePublication')[:6]  # Récupère les 6 dernières annonces
    return render(request, 'base.html', {'annonces': annonces, 'MEDIA_URL': settings.MEDIA_URL,"categories":categories})

from django.shortcuts import get_object_or_404

class detail_annonce(View):
    def get(self, request, annonce_id):
        annonce = get_object_or_404(Annonce, id=annonce_id)
        return render(request, 'Utilisateur/detail_annonce.html',
                       {'annonce': annonce,
                        'user_ads_count': Annonce.objects.filter(user_id = request.user.id).count(),
                        'MEDIA_URL': settings.MEDIA_URL})

class EnvoyerMessageAuUser(View):
    def get(self,request,user_id):
        userMessages = Message.objects.filter(userIdSource=request.user.id,userIdDesti=user_id)
        user_des = User.objects.get(id = user_id)
        return render(request,"Utilisateur/interfaceChat.html",{"user_actif":user_des,"userMessages":userMessages})
    
    def post(self,request,user_id):
        contenu = request.POST.get("contenu")
        user_des = request.POST.get("user_id")
        print(user_des)
        Message.objects.create(
            userIdDesti_id = user_des,
            contenu=contenu,
            userIdSource_id = request.user.id,
        )
        return redirect(f"/user/messages/{user_id}")
    
def messageUserAuUser(request,user_id):
    print(user_id)
    # return HttpResponse(user_id)
    listeUser = Message.objects.filter(userIdSource = request.user.id)
    # # user = User.objects.get(id=userid)
    userMessages = Message.objects.filter(userIdSource=request.user.id,userIdDesti=user_id)
    return render(request,"Utilisateur/interfaceChat.html",{"listeUser":listeUser})




#admin views

class LoginPageAdmin(View):
   def get(self, request):
    return render(request, 'Administrateur/login.html')

def register_admin(request):
    if request.method == 'POST':
        form = BaseProfileFormAdmin(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = BaseProfileFormAdmin()
    return render(request, 'Administrateur/register.html', {'form': form})

class AuthAdministrateur(View):
    def _get_common_context(self, user):
        """Génère le contexte commun pour les deux méthodes (GET et POST)"""
        return {
            'annonces': Annonce.objects.all().order_by('-datePublication')[:6],
            'annonce_validee':Annonce.objects.filter(statut = 'active').count(),
            'annonce_non_validee':Annonce.objects.exclude(statut = 'active').count(),
            'Annonces_en_attentes':Annonce.objects.exclude(statut = 'active'),
            'MEDIA_URL': settings.MEDIA_URL,
            'categories': Categorie.objects.all(),
            'Admin': user,
            'user': User.objects.all(),
            'user_count': User.objects.all().count(),
            
        }

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = authenticate(request, username=email, password=password)
        
        if admin is not None:
            login(request, admin)
            return render(request, 'Administrateur/homePage.html', self._get_common_context(admin))
        else:
            messages.error(request, 'Email ou mot de passe invalide.')
            return redirect('login_admin')

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'Administrateur/homePage.html', self._get_common_context(request.user))
        return redirect('login_admin')

def Profil_Admin(request, Admin_id):
    return render(request, 'Administrateur/Profil_Admin.html', {
        'Admin': get_object_or_404(Administrateur, id=Admin_id),
        # 'user_favorites_count': fa.objects.filter(user_id = request.user.id).count(),
        'MEDIA_URL':settings.MEDIA_URL
    })

def get_Utilisateur(request):
    
    context = {
        'users': [
            {
                'id': user.id,
                'image': user.image,
                'nom': user.nom,
                'prenom': user.prenom,   # Meilleure pratique que user.nom
                'email': user.email,
                'is_active': user.is_active,
                'annonces_validees': user.annonces.filter(statut = 'active').count(), 
                'annonces_non_validees': user.annonces.exclude(statut = 'active').count(), 
                'last_login': user.last_login,  # Ajout utile pour l'admin
                'date_joined': user.date_joined,  # Ajout utile pour l'admin
            }
            for user in User.objects.all()
        ],
        'total_users': User.objects.all().count(),  # Ajout statistique utile
        'active_users': User.objects.filter(is_active=True).count(),  # Ajout statistique
    }
    
    return render(request, 'Administrateur/Utilisateurs.html', context)

def get_Utilisateur_Profil(request, user_id):


    annonces_enatt = Annonce.objects.filter(user_id = user_id, statut = 'en_attente')
    annonces_val = Annonce.objects.filter(user_id = user_id, statut = 'active')


    return render(request, 'Administrateur/Details_utilisateur.html', {
        'user': get_object_or_404(User, id=user_id),
        'annonces_val': annonces_val,
        'annonces_enatt':annonces_enatt,
        'annonces_validees': Annonce.objects.filter(user_id = user_id, statut = 'active').count(),
        'annonces_non_validees': Annonce.objects.filter(user_id = user_id, statut = 'en_attente').count(),
        'categories' : Categorie.objects.all(),
        'MEDIA_URL':settings.MEDIA_URL
    })

def preview_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    context = {
        'annonce': annonce,
        'MEDIA_URL': settings.MEDIA_URL
    }
    return render(request, 'Administrateur/previsualiser_annonce.html', context)

from django.core.mail import send_mail
from django.contrib import messages

def approve_annonce(request):
    if request.method == 'POST':
        annonce = get_object_or_404(Annonce, id=request.POST.get('annonce_id'))
        annonce.statut = 'active'
        annonce.save()
        
        # Envoi d'email
        send_mail(
            subject=f"Annonce approuvée : {annonce.titre}",
            message=f"Votre annonce '{annonce.titre}' a été approuvée.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[annonce.user.email]
        )
        
        messages.success(request, "L'annonce a été approuvée avec succès.")
        return redirect('home_admin')
    
    messages.error(request, "L'annonce n'a pas été approuvée .")
    return redirect('home_admin')

def reject_annonce(request):
    if request.method == 'POST':
        annonce = get_object_or_404(Annonce, id=request.POST.get('annonce_id'))
        reason = request.POST.get('rejection_reason', 'Raison non spécifiée')

        # Envoi d'email
        send_mail(
            subject=f"Annonce rejetée : {annonce.titre}",
            message=f"Votre annonce a été rejetée. Raison : {reason}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[annonce.user.email],  
        )
        
        annonce.delete()
        messages.success(request, "L'annonce a été rejetée avec succès.")
        return redirect('home_admin')
    
    messages.error(request, "L'annonce n'a pas été rejetée.")
    return redirect('home_admin')