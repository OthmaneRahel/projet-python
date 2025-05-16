
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
from .models import User, Message,Categorie
from .forms import BaseProfileForm, InscriptionForm
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
            return redirect('login')
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
            return render(request, 'Utilisateur/homePage.html')  # Redirection après succès
        else:
            messages.error(request, 'Email ou mot de passe invalide.')
            return redirect('login_page')  # On retourne à la page de connexion

    def get(self, request):
        # if request.user.is_authenticated:
        #     return render(request, 'Utilisateur/homePage.html')  # Redirige vers la page d'accueil si déjà connecté
        return redirect('login_page')

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

def ajouter_annonce(request):
    if request.method == 'POST':
            titre = request.POST.get('titre')
            description = request.POST.get('description')
            categorie = request.POST.get('categorie_id')
            prix = float(request.POST.get('prix'))
            is_premieum = request.POST.get('isPremieum') == 'on'
            noms_images = []
            images = request.FILES.getlist('images')
            for image in images:
                path = os.path.join('annonces', image.name)
                saved_path = default_storage.save(path, image)
                noms_images.append(saved_path)
            annonce = Annonce.objects.create(
                titre=titre,
                description=description,
                prix=prix,
                user_id=request.user.id,
                categorie_id=categorie,
                isPremieum=is_premieum,
                statut='active',
                images=noms_images
            )
            return JsonResponse({'success': True, 'annonce_id': annonce.id})
    
def afficher_annonce_categorie(request,categorie_id):

    annonces = Annonce.objects.filter(categorie_id=categorie_id)
    return render(request, 'Utilisateur/test.html', {
        'annonces': annonces,
        'MEDIA_URL': settings.MEDIA_URL
})

from .models import Annonce

def home(request):
    categories = Categorie.objects.all()
    annonces = Annonce.objects.all().order_by('-datePublication')[:6]  # Récupère les 6 dernières annonces
    return render(request, 'base.html', {'annonces': annonces, 'MEDIA_URL': settings.MEDIA_URL,"categories":categories})

from django.shortcuts import get_object_or_404

# def detail_annonce(request, annonce_id):
#     annonce = get_object_or_404(Annonce, id=annonce_id)
#     return render(request, 'Utilisateur/detail_annonce.html', {
#         'annonce': annonce,
#         'MEDIA_URL': settings.MEDIA_URL
#     })

class detail_annonce(View):
    def get(self, request, annonce_id):
        annonce = get_object_or_404(Annonce, id=annonce_id)
        return render(request, 'Utilisateur/detail_annonce.html', {'annonce': annonce, 'MEDIA_URL': settings.MEDIA_URL})

class EnvoyerMessageAuUser(View):
    def get(self,request,user_id):
        userMessages = Message.objects.filter(userIdSource=request.user.id,userIdDesti=user_id)
        user_des = User.objects.get(id = user_id);
        return render(request,"Utilisateur/interfaceChat.html",{"user_actif":user_des,"userMessages":userMessages})
    def post(self,request,user_id):
        contenu = request.POST.get("contenu")
        user_des = request.POST.get("user_id")
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