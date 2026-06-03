from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_conversations, name='liste_conversations'),
    path('<int:conv_id>/', views.detail_conversation, name='detail_conversation'),
    path('demarrer/<int:user_id>/', views.demarrer_conversation, name='demarrer_conversation'),
    path('<int:conv_id>/envoyer/', views.envoyer_message, name='envoyer_message'),
    path('<int:conv_id>/nouveaux/', views.nouveaux_messages, name='nouveaux_messages'),
]
