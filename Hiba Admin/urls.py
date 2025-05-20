from django.urls import path
from . import views 



urlpatterns=[
    #Utilisateur
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



    #Admin

    path('inscription_Admin/', views.register_admin ,name='inscription_Admin'),
    path('login_adm/', views.LoginPageAdmin.as_view(), name='login_admin'),           # GET: formulaire
    path('home_Admin/', views.AuthAdministrateur.as_view(), name='home_admin'),
    path('logout/', views.LogoutView.as_view(), name='logout'),


    path('Profil_Admin/<int:Admin_id>', views.Profil_Admin, name='Profil_Admin'),
    path('Profil_Modifier_Admin/', views.Profil_modifier, name='Profil_Modifier_Admin'),

    path('Utilisateurs/',views.get_Utilisateur,name='Utilisateurs'),
    path('Utilisateur/<int:user_id>',views.get_Utilisateur_Profil,name='Utilisateur'),

    path('preview/<int:annonce_id>/', views.preview_annonce, name='preview_annonce'),
    path('approve/', views.approve_annonce, name='approve_annonce'),
    path('reject/', views.reject_annonce, name='reject_annonce'),

]