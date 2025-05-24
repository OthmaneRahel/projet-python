
import os
# from django.dispatch import Signals
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from .forms import InscriptionForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Favoris, User, Message,Categorie, Annonce, Signal
from .forms import BaseProfileForm, InscriptionForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
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
            return redirect('home')  # On retourne à la page de connexion

    def get(self, request):
        if request.user.is_authenticated:
            categories = Categorie.objects.all()
            annonces = Annonce.objects.all().order_by('-datePublication')[:6]  # Récupère les 6 dernières annonces
            signal = Signal.objects.filter(user_id=request.user.id)
            signal_annonce = Signal.objects.raw("SELECT s.* , a.* FROM app_signal s JOIN app_annonce a ON s.annonce_id = a.id")
            
            return render(request, 'Utilisateur/homePage.html',{'annonces': annonces, 'MEDIA_URL': settings.MEDIA_URL,"categories":categories,"signal":signal,"signal_annonce":signal_annonce})  # Redirection après succès
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

# def home(request):
#     categories = Categorie.objects.all()
#     annonces = Annonce.objects.all().order_by('-datePublication')[:6]  # Récupère les 6 dernières annonces
#     return render(request, 'base.html', {'annonces': annonces, 'MEDIA_URL': settings.MEDIA_URL,"categories":categories})

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
    
    # return HttpResponse(user_id)
    listeUser = Message.objects.filter(userIdSource = request.user.id)
    # # user = User.objects.get(id=userid)
    userMessages = Message.objects.filter(userIdSource=request.user.id,userIdDesti=user_id)
    return render(request,"Utilisateur/interfaceChat.html",{"listeUser":listeUser})

class AjouterAuxFavoris(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, annonce_id):
        annonce = get_object_or_404(Annonce, id=annonce_id)
        
        if annonce is not None:
            favori_existant = Favoris.objects.filter(user_id=request.user.id, annonce_id=annonce.id).first()
            
            if not favori_existant:
                # Create a new favorite entry
                Favoris.objects.create(user_id=request.user.id, annonce_id=annonce.id)
                messages.success(request, 'Annonce ajouté aux favoris avec succès!')
                return redirect('favoris') 
            
            else:
                messages.info(request, 'Ce annonce est déjà dans vos favoris.')
                return redirect('home_user')
                # categories = Categorie.objects.all()
                # annonces = Annonce.objects.all().order_by('-datePublication')[:6]  # Récupère les 6 dernières annonces
                # return render(request, 'Utilisateur/homePage.html',{'annonces': annonces, 'MEDIA_URL': settings.MEDIA_URL,"categories":categories})  # Redirection après succès
        else:
            messages.error(request, 'Annonce non trouvé.')
            return redirect('home_user')
        
class SupprimerDesFavoris(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, annonce_id):
        favori_item = get_object_or_404(Favoris, user_id=request.user.id, annonce_id=annonce_id)
        favori_item.delete()
        messages.success(request, 'Annonce retiré des favoris avec succès!')
        return redirect('favoris')
    
class AfficherFavoris(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        favoris = Favoris.objects.filter(user=request.user).select_related('annonce')
        return render(request, 'Utilisateur/favoris.html', {
            'favoris': favoris,
            'MEDIA_URL': settings.MEDIA_URL
        })

def rechercher_annonce(request):
    query = request.GET.get('q', '')
    
    if query:
        Annonces = Annonce.objects.filter(
            Q(titre__icontains=query) )
        paginator = Paginator(Annonces, 8)  # Show 10 books per page
        page_number = request.GET.get('page')
        annonces = paginator.get_page(page_number)
    else:
        Annonces = Annonces.objects.all()
        paginator = Paginator(Annonces, 8)  # Show 10 books per page
        page_number = request.GET.get('page')
        annonces = paginator.get_page(page_number)

    return render(request, 'Utilisateur/homePage.html', {'annonces': annonces, 'query': query, 'MEDIA_URL': settings.MEDIA_URL}) 

from django.shortcuts import redirect
from django.contrib import messages

def signaler_annonce(request):
    if request.method == 'POST':
        annonce_id = request.POST.get('annonce_id')
        raison = request.POST.get('raison')
        
        if not annonce_id or not raison:
            messages.error(request, "Veuillez fournir une raison de signalement")
            return redirect('home_user')
        
        try:
            annonce = Annonce.objects.get(id=annonce_id)
            # Créer le signalement
            Signal.objects.create(
                description=raison,
                user_id=request.user.id,
                annonce_id=annonce_id
            )
            

            messages.success(request, "L'annonce a été signalée et sera examinée")
            return redirect('home_user')
            
        except Annonce.DoesNotExist:
            messages.error(request, "Annonce non trouvée")
            return redirect('home_user')
    
    return redirect('home_user')

def home(request):
    categories = Categorie.objects.all()
    annonces = Annonce.objects.exclude(statut='signale').order_by('-datePublication')[:6]
    return render(request, 'base.html', {
        'annonces': annonces, 
        'MEDIA_URL': settings.MEDIA_URL,
        "categories": categories
    })