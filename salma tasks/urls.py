from django.urls import path
from . import views 


urlpatterns=[
    path('',views.home,name='home'),
    path('inscription/', views.inscription ,name='inscription'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('home/', views.AuthUtilisateur.as_view(), name='home_user'),

    path('login/', views.LoginPage.as_view(), name='login_page'),           # GET: formulaire
    path('login/submit/',views. AuthUtilisateur.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('annonces/ajouter/', views.ajouter_annonce, name='ajouter_annonce'),
    path('annonces/', views.afficher_annonce_categorie, name='liste_annonce'),

    path('annonce/<int:annonce_id>/', views.detail_annonce.as_view(), name='detail_annonce'),

    path('Profil_User/<int:user_id>', views.Profil_User, name='Profil_User'),
    path('Profil_Modifier/', views.Profil_modifier, name='Profil_Modifier'),

    path('user/messages/<int:user_id>',views.EnvoyerMessageAuUser.as_view(), name='messageToUser'),
    path('message/<user_id>',views.messageUserAuUser, name='chat_actif'),

]