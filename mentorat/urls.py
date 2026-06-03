from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_de_bord, name='tableau_de_bord'),
    path('matching/', views.lancer_matching, name='lancer_matching'),
    path('publications/', views.liste_publications, name='liste_publications'),
    path('publications/creer/', views.creer_publication, name='creer_publication'),
    path('publications/<int:pub_id>/', views.detail_publication, name='detail_publication'),
    path('publications/<int:pub_id>/supprimer/', views.supprimer_publication, name='supprimer_publication'),
    path('matching/<int:match_id>/accepter/', views.accepter_matching, name='accepter_matching'),
    path('matching/<int:match_id>/refuser/', views.refuser_matching, name='refuser_matching'),
]
