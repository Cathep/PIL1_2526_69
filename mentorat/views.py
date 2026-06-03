from datetime import date, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import DemandeOuOffre, Matching
from comptes.models import Utilisateur, Competence, CompetenceUtilisateur, Disponibilite


@login_required
def tableau_de_bord(request):
    # suggestions de matching pour l'utilisateur connecte
    mes_matchings = Matching.objects.filter(
        Q(mentor=request.user) | Q(mentore=request.user)
    ).select_related('mentor', 'mentore').order_by('-score_global')[:5]

    mes_publications = DemandeOuOffre.objects.filter(
        auteur=request.user, statut='ouvert'
    ).select_related('competence').order_by('-date_creation')[:5]

    contexte = {
        'matchings': mes_matchings,
        'publications': mes_publications,
        'utilisateur': request.user,
    }
    return render(request, 'mentorat/tableau_de_bord.html', contexte)


@login_required
def lancer_matching(request):
    utilisateur = request.user

    mes_forces = set(utilisateur.competences.filter(type_competence='force').values_list('competence_id', flat=True))
    mes_lacunes = set(utilisateur.competences.filter(type_competence='lacune').values_list('competence_id', flat=True))
    mes_dispos = list(utilisateur.disponibilites.all())

    autres_utilisateurs = Utilisateur.objects.filter(is_active=True).exclude(id=utilisateur.id)
    resultats = []

    def overlap_minutes(dispo_a, dispo_b):
        if dispo_a.jour != dispo_b.jour:
            return 0
        debut = max(dispo_a.heure_debut, dispo_b.heure_debut)
        fin = min(dispo_a.heure_fin, dispo_b.heure_fin)
        if debut >= fin:
            return 0
        delta = datetime.combine(date.today(), fin) - datetime.combine(date.today(), debut)
        return max(delta.total_seconds() / 60, 0)

    def total_minutes(dispos):
        total = 0
        for dispo in dispos:
            delta = datetime.combine(date.today(), dispo.heure_fin) - datetime.combine(date.today(), dispo.heure_debut)
            total += max(delta.total_seconds() / 60, 0)
        return max(total, 1)

    total_mes_minutes = total_minutes(mes_dispos)

    for autre in autres_utilisateurs:
        if utilisateur.role == 'mentor' and autre.role == 'mentor':
            continue
        if utilisateur.role == 'mentore' and autre.role == 'mentore':
            continue

        forces_autre = set(autre.competences.filter(type_competence='force').values_list('competence_id', flat=True))
        lacunes_autre = set(autre.competences.filter(type_competence='lacune').values_list('competence_id', flat=True))
        dispos_autre = list(autre.disponibilites.all())

        correspondances_mentor = len(mes_lacunes & forces_autre)
        correspondances_mentore = len(mes_forces & lacunes_autre)
        total_possible = max(len(mes_lacunes) + len(lacunes_autre), 1)
        score_comp = ((correspondances_mentor + correspondances_mentore) / total_possible) * 100

        common_minutes = sum(overlap_minutes(a, b) for a in mes_dispos for b in dispos_autre)
        total_autre_minutes = total_minutes(dispos_autre)
        score_horaires = (common_minutes / max(total_mes_minutes, total_autre_minutes, 1)) * 100

        if utilisateur.filiere_id and autre.filiere_id:
            score_filiere = 100 if utilisateur.filiere_id == autre.filiere_id else 40
        else:
            score_filiere = 0

        if utilisateur.niveau and autre.niveau:
            score_niveau = 100 if utilisateur.niveau == autre.niveau else 40
        else:
            score_niveau = 0

        score_global = (
            score_comp * 0.45 +
            score_horaires * 0.30 +
            score_filiere * 0.15 +
            score_niveau * 0.10
        )

        if score_global > 10:
            if utilisateur.role == 'mentor' and autre.role in ['mentore', 'les_deux']:
                mentor, mentore = utilisateur, autre
            elif utilisateur.role == 'mentore' and autre.role in ['mentor', 'les_deux']:
                mentor, mentore = autre, utilisateur
            elif utilisateur.role == 'les_deux' and autre.role == 'mentor':
                mentor, mentore = autre, utilisateur
            elif utilisateur.role == 'les_deux' and autre.role == 'mentore':
                mentor, mentore = utilisateur, autre
            else:
                if correspondances_mentor >= correspondances_mentore:
                    mentor, mentore = autre, utilisateur
                else:
                    mentor, mentore = utilisateur, autre

            matching, created = Matching.objects.update_or_create(
                mentor=mentor,
                mentore=mentore,
                defaults={
                    'score_global': round(score_global, 2),
                    'score_competences': round(score_comp, 2),
                    'score_horaires': round(score_horaires, 2),
                    'score_filiere': round(score_filiere, 2),
                }
            )
            resultats.append(matching)

    resultats.sort(key=lambda m: m.score_global, reverse=True)

    return render(request, 'mentorat/resultats_matching.html', {
        'resultats': resultats[:20],
        'utilisateur': utilisateur,
    })


@login_required
def liste_publications(request):
    type_filtre = request.GET.get('type', '')
    competence_filtre = request.GET.get('competence', '')
    jour_filtre = request.GET.get('jour', '')

    publications = DemandeOuOffre.objects.filter(statut='ouvert').exclude(
        auteur=request.user
    ).select_related('auteur', 'competence').order_by('-date_creation')

    if type_filtre:
        publications = publications.filter(type_publication=type_filtre)
    if competence_filtre:
        publications = publications.filter(competence_id=competence_filtre)
    if jour_filtre:
        publications = publications.filter(jour=jour_filtre)

    competences = Competence.objects.all().order_by('nom')
    jours = Disponibilite.JOURS

    return render(request, 'mentorat/liste_publications.html', {
        'publications': publications,
        'competences': competences,
        'type_filtre': type_filtre,
        'competence_filtre': competence_filtre,
        'jour_filtre': jour_filtre,
        'jours': jours,
    })


@login_required
def creer_publication(request):
    if request.method == 'POST':
        type_pub = request.POST.get('type_publication')
        competence_id = request.POST.get('competence')
        format_seance = request.POST.get('format_seance')
        jour = request.POST.get('jour') or None
        heure_debut = request.POST.get('heure_debut') or None
        heure_fin = request.POST.get('heure_fin') or None
        description = request.POST.get('description', '')

        if not type_pub or not competence_id or not format_seance:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        elif jour and (not heure_debut or not heure_fin):
            messages.error(request, "Veuillez indiquer une plage horaire complète pour le jour choisi.")
        else:
            DemandeOuOffre.objects.create(
                auteur=request.user,
                type_publication=type_pub,
                competence_id=competence_id,
                format_seance=format_seance,
                jour=jour,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                description=description
            )
            messages.success(request, "Votre publication a été créée avec succès !")
            return redirect('liste_publications')

    competences = Competence.objects.all().order_by('categorie', 'nom')
    jours = Disponibilite.JOURS
    return render(request, 'mentorat/creer_publication.html', {'competences': competences, 'jours': jours})


@login_required
def detail_publication(request, pub_id):
    publication = get_object_or_404(DemandeOuOffre, id=pub_id)
    return render(request, 'mentorat/detail_publication.html', {'publication': publication})


@login_required
def supprimer_publication(request, pub_id):
    publication = get_object_or_404(DemandeOuOffre, id=pub_id, auteur=request.user)
    publication.delete()
    messages.success(request, "Publication supprimée.")
    return redirect('liste_publications')


@login_required
def accepter_matching(request, match_id):
    matching = get_object_or_404(
        Matching,
        id=match_id,
        statut='en_attente'
    )
    # verifier que l'utilisateur fait partie du matching
    if request.user not in [matching.mentor, matching.mentore]:
        messages.error(request, "Vous n'êtes pas autorisé à effectuer cette action.")
        return redirect('tableau_de_bord')

    matching.statut = 'accepte'
    matching.save()

    # creer automatiquement une conversation
    from messagerie.models import Conversation
    Conversation.get_ou_creer(matching.mentor, matching.mentore, matching)

    messages.success(request, "Matching accepté ! Vous pouvez maintenant discuter.")
    return redirect('tableau_de_bord')


@login_required
def refuser_matching(request, match_id):
    matching = get_object_or_404(Matching, id=match_id)
    if request.user not in [matching.mentor, matching.mentore]:
        messages.error(request, "Action non autorisée.")
        return redirect('tableau_de_bord')

    matching.statut = 'refuse'
    matching.save()
    messages.info(request, "Matching refusé.")
    return redirect('tableau_de_bord')
