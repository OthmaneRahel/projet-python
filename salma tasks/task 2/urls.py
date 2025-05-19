from django.urls import path
from . import views 



urlpatterns=[
    path('',views.home,name='home'),
    path('inscription/', views.inscription ,name='inscription'),

    path('login/', views.LoginPage.as_view(), name='login_page'),           # GET: formulaire
    path('home/', views.AuthUtilisateur.as_view(), name='home_user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('annonces/ajouter/', views.ajouter_annonce, name='ajouter_annonce'),
    path('annonces/', views.afficher_annonce_categorie, name='liste_annonce'),
    path('mes-annonces/', views.mes_annonces, name='mes_annonces'),
    path('modifier_annonce/<int:annonce_id>/', views.modifier_annonce, name='modifier_annonce'),

    path('annonce/<int:annonce_id>/', views.detail_annonce.as_view(), name='detail_annonce'),

    path('Profil_User/<int:user_id>', views.Profil_User, name='Profil_User'),
    path('Profil_Modifier/', views.Profil_modifier, name='Profil_Modifier'),

    path('user/messages/<int:user_id>',views.EnvoyerMessageAuUser.as_view(), name='messageToUser'),
    path('message/<user_id>',views.messageUserAuUser, name='chat_actif'),

    path('ajouter_favoris/<int:annonce_id>/', views.AjouterAuxFavoris.as_view(), name='ajouter_favoris'),
    path('supprimer_favoris/<int:annonce_id>/', views.SupprimerDesFavoris.as_view(), name='supprimer_des_favoris'),
    path('favoris/', views.AfficherFavoris.as_view(), name='favoris'),

    path('recherche/', views.rechercher_annonce, name='rechercher_annonce'),

    path('signaler/', views.signaler_annonce, name='signaler_annonce'),

]