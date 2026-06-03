from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_connexion, name='connexion'),
    path('inscription/', views.page_inscription, name='inscription'),
    path('mot-de-passe-oublie/', views.demander_reinitialisation, name='demander_reinitialisation'),
    path('mot-de-passe/reinitialiser/<str:token>/', views.reinitialiser_mot_de_passe, name='reinitialiser_mot_de_passe'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/completer/', views.completer_profil, name='completer_profil'),
    path('profil/', views.mon_profil, name='mon_profil'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('profil/<int:user_id>/', views.voir_profil, name='voir_profil'),
]
