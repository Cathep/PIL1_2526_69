from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Max
from .models import Conversation, Message
from comptes.models import Utilisateur
import json


@login_required
def liste_conversations(request):
    # recuperer toutes les conversations de l'utilisateur
    conversations = Conversation.objects.filter(
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user)
    ).annotate(
        dernier_message=Max('messages__date_envoi')
    ).order_by('-dernier_message')

    # enrichir avec le dernier message et les non lus
    conv_enrichies = []
    for conv in conversations:
        autre = conv.utilisateur2 if conv.utilisateur1 == request.user else conv.utilisateur1
        dernier_msg = conv.messages.order_by('-date_envoi').first()
        non_lus = conv.messages.filter(lu=False).exclude(expediteur=request.user).count()
        conv_enrichies.append({
            'conversation': conv,
            'autre_utilisateur': autre,
            'dernier_message': dernier_msg,
            'non_lus': non_lus,
        })

    return render(request, 'messagerie/liste_conversations.html', {
        'conversations': conv_enrichies
    })


@login_required
def detail_conversation(request, conv_id):
    conversation = get_object_or_404(
        Conversation,
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user),
        id=conv_id
    )

    # marquer les messages comme lus
    conversation.messages.filter(lu=False).exclude(expediteur=request.user).update(lu=True)

    autre = conversation.utilisateur2 if conversation.utilisateur1 == request.user else conversation.utilisateur1
    msgs = conversation.messages.select_related('expediteur').order_by('date_envoi')

    return render(request, 'messagerie/conversation.html', {
        'conversation': conversation,
        'messages': msgs,
        'autre_utilisateur': autre,
    })


@login_required
def demarrer_conversation(request, user_id):
    autre = get_object_or_404(Utilisateur, id=user_id, is_active=True)
    if autre == request.user:
        messages.error(request, "Vous ne pouvez pas vous envoyer un message à vous-même.")
        return redirect('tableau_de_bord')

    conv = Conversation.get_ou_creer(request.user, autre)
    return redirect('detail_conversation', conv_id=conv.id)


@login_required
@require_POST
def envoyer_message(request, conv_id):
    conversation = get_object_or_404(
        Conversation,
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user),
        id=conv_id
    )

    contenu = request.POST.get('contenu', '').strip()
    if not contenu:
        return JsonResponse({'erreur': 'Message vide'}, status=400)

    message = Message.objects.create(
        conversation=conversation,
        expediteur=request.user,
        contenu=contenu
    )

    # reponse JSON pour la mise a jour en temps reel
    return JsonResponse({
        'id': message.id,
        'contenu': message.contenu,
        'expediteur': request.user.nom_complet(),
        'date_envoi': message.date_envoi.strftime('%H:%M'),
        'est_moi': True,
    })


@login_required
def nouveaux_messages(request, conv_id):
    # endpoint pour verifier s'il y a de nouveaux messages (polling)
    dernier_id = int(request.GET.get('dernier_id', 0))

    conversation = get_object_or_404(
        Conversation,
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user),
        id=conv_id
    )

    nouveaux = conversation.messages.filter(
        id__gt=dernier_id
    ).exclude(expediteur=request.user).select_related('expediteur')

    # marquer comme lus
    nouveaux.update(lu=True)

    data = [{
        'id': msg.id,
        'contenu': msg.contenu,
        'expediteur': msg.expediteur.nom_complet(),
        'date_envoi': msg.date_envoi.strftime('%H:%M'),
        'est_moi': False,
    } for msg in nouveaux]

    return JsonResponse({'messages': data})
