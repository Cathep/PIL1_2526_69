import secrets
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models import Utilisateur, Filiere, Competence, CompetenceUtilisateur, Disponibilite
from .forms import (
    FormulaireInscription,
    FormulaireConnexion,
    FormulaireProfilBase,
    FormulaireProfilCompetences,
    FormulaireResetPasswordDemande,
    FormulaireResetPassword,
)


def page_inscription(request):
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')

    if request.method == 'POST':
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            messages.success(request, f"Bienvenue {utilisateur.prenom} ! Votre compte a été créé.")
            return redirect('completer_profil')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = FormulaireInscription()

    return render(request, 'comptes/inscription.html', {'form': form})


def page_connexion(request):
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')

    if request.method == 'POST':
        form = FormulaireConnexion(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data['identifiant'].strip()
            mot_de_passe = form.cleaned_data['mot_de_passe']
            utilisateur = None
            if '@' in identifiant:
                utilisateur = Utilisateur.objects.filter(email__iexact=identifiant).first()
            else:
                utilisateur = Utilisateur.objects.filter(telephone=identifiant).first()

            if utilisateur:
                utilisateur = authenticate(request, username=utilisateur.email, password=mot_de_passe)
                if utilisateur:
                    login(request, utilisateur)
                    return redirect('tableau_de_bord')

            messages.error(request, "Identifiant ou mot de passe incorrect.")
    else:
        form = FormulaireConnexion()

    return render(request, 'comptes/connexion.html', {'form': form})


def deconnexion(request):
    logout(request)
    return redirect('connexion')


def demander_reinitialisation(request):
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')

    if request.method == 'POST':
        form = FormulaireResetPasswordDemande(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data['identifiant'].strip()
            utilisateur = None
            if '@' in identifiant:
                utilisateur = Utilisateur.objects.filter(email__iexact=identifiant).first()
            else:
                utilisateur = Utilisateur.objects.filter(telephone=identifiant).first()

            if utilisateur:
                token = secrets.token_urlsafe(20)
                utilisateur.token_reinitialisation = token
                utilisateur.token_expire_le = timezone.now() + timedelta(hours=1)
                utilisateur.save(update_fields=['token_reinitialisation', 'token_expire_le'])
                lien = request.build_absolute_uri(reverse('reinitialiser_mot_de_passe', args=[token]))
                subject = 'Réinitialisation de votre mot de passe MentorLink'
                message = (
                    f'Bonjour {utilisateur.prenom},\n\n'
                    f'Pour réinitialiser votre mot de passe MentorLink, cliquez sur le lien ci-dessous :\n{lien}\n\n'
                    'Si vous n’avez pas demandé cette réinitialisation, ignorez ce message.\n\n'
                    'Cordialement,\nL’équipe MentorLink'
                )
                send_mail(subject, message, None, [utilisateur.email])
                messages.success(request, "Un email de réinitialisation a été envoyé si le compte existe.")
                if settings.DEBUG:
                    messages.info(request, f"Lien de test : {lien}")
                return redirect('connexion')
            messages.error(request, "Aucun compte trouvé pour cet identifiant.")
    else:
        form = FormulaireResetPasswordDemande()

    return render(request, 'comptes/reset_password_request.html', {'form': form})


def reinitialiser_mot_de_passe(request, token):
    utilisateur = get_object_or_404(
        Utilisateur,
        token_reinitialisation=token,
        token_expire_le__gte=timezone.now()
    )

    if request.method == 'POST':
        form = FormulaireResetPassword(request.POST)
        if form.is_valid():
            utilisateur.set_password(form.cleaned_data['mot_de_passe'])
            utilisateur.token_reinitialisation = ''
            utilisateur.token_expire_le = None
            utilisateur.save(update_fields=['password', 'token_reinitialisation', 'token_expire_le'])
            messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
            return redirect('connexion')
    else:
        form = FormulaireResetPassword()

    return render(request, 'comptes/reset_password_confirm.html', {
        'form': form,
        'token': token,
    })


@login_required
def completer_profil(request):
    # etape 2 apres inscription : choisir competences et dispos
    filieres = Filiere.objects.all()
    competences = Competence.objects.all().order_by('categorie', 'nom')

    if request.method == 'POST':
        # infos de base
        request.user.filiere_id = request.POST.get('filiere')
        request.user.niveau = request.POST.get('niveau')
        request.user.role = request.POST.get('role')
        request.user.bio = request.POST.get('bio', '')
        if request.FILES.get('photo_profil'):
            request.user.photo_profil = request.FILES['photo_profil']
        request.user.save()

        # points forts
        forces = request.POST.getlist('forces')
        for comp_id in forces:
            CompetenceUtilisateur.objects.get_or_create(
                utilisateur=request.user,
                competence_id=comp_id,
                type_competence='force'
            )

        # lacunes
        lacunes = request.POST.getlist('lacunes')
        for comp_id in lacunes:
            CompetenceUtilisateur.objects.get_or_create(
                utilisateur=request.user,
                competence_id=comp_id,
                type_competence='lacune'
            )

        # disponibilites
        jours = request.POST.getlist('jours')
        heures_debut = request.POST.getlist('heure_debut')
        heures_fin = request.POST.getlist('heure_fin')
        for i, jour in enumerate(jours):
            if jour and heures_debut[i] and heures_fin[i]:
                Disponibilite.objects.create(
                    utilisateur=request.user,
                    jour=jour,
                    heure_debut=heures_debut[i],
                    heure_fin=heures_fin[i]
                )

        messages.success(request, "Profil complété avec succès !")
        return redirect('tableau_de_bord')

    contexte = {
        'filieres': filieres,
        'competences': competences,
        'niveaux': Utilisateur.NIVEAUX,
        'roles': Utilisateur.ROLES,
        'jours': Disponibilite.JOURS,
    }
    return render(request, 'comptes/completer_profil.html', contexte)


@login_required
def mon_profil(request):
    competences_forces = request.user.competences.filter(type_competence='force').select_related('competence')
    competences_lacunes = request.user.competences.filter(type_competence='lacune').select_related('competence')
    disponibilites = request.user.disponibilites.all()

    contexte = {
        'utilisateur': request.user,
        'forces': competences_forces,
        'lacunes': competences_lacunes,
        'disponibilites': disponibilites,
    }
    return render(request, 'comptes/profil.html', contexte)


@login_required
def modifier_profil(request):
    if request.method == 'POST':
        request.user.nom = request.POST.get('nom', request.user.nom)
        request.user.prenom = request.POST.get('prenom', request.user.prenom)
        request.user.telephone = request.POST.get('telephone', request.user.telephone)
        request.user.bio = request.POST.get('bio', '')
        request.user.filiere_id = request.POST.get('filiere')
        request.user.niveau = request.POST.get('niveau')
        request.user.role = request.POST.get('role')
        if request.FILES.get('photo_profil'):
            request.user.photo_profil = request.FILES['photo_profil']
        request.user.save()

        # mise a jour des competences
        request.user.competences.all().delete()
        for comp_id in request.POST.getlist('forces'):
            CompetenceUtilisateur.objects.create(
                utilisateur=request.user, competence_id=comp_id, type_competence='force'
            )
        for comp_id in request.POST.getlist('lacunes'):
            CompetenceUtilisateur.objects.create(
                utilisateur=request.user, competence_id=comp_id, type_competence='lacune'
            )

        # mise a jour des disponibilites
        request.user.disponibilites.all().delete()
        jours = request.POST.getlist('jours')
        heures_debut = request.POST.getlist('heure_debut')
        heures_fin = request.POST.getlist('heure_fin')
        for i, jour in enumerate(jours):
            if jour and heures_debut[i] and heures_fin[i]:
                Disponibilite.objects.create(
                    utilisateur=request.user,
                    jour=jour,
                    heure_debut=heures_debut[i],
                    heure_fin=heures_fin[i]
                )

        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('mon_profil')

    filieres = Filiere.objects.all()
    competences = Competence.objects.all().order_by('categorie', 'nom')
    forces_ids = list(request.user.competences.filter(type_competence='force').values_list('competence_id', flat=True))
    lacunes_ids = list(request.user.competences.filter(type_competence='lacune').values_list('competence_id', flat=True))

    contexte = {
        'utilisateur': request.user,
        'filieres': filieres,
        'competences': competences,
        'forces_ids': forces_ids,
        'lacunes_ids': lacunes_ids,
        'disponibilites': request.user.disponibilites.all(),
        'niveaux': Utilisateur.NIVEAUX,
        'roles': Utilisateur.ROLES,
        'jours': Disponibilite.JOURS,
    }
    return render(request, 'comptes/modifier_profil.html', contexte)


@login_required
def voir_profil(request, user_id):
    # voir le profil d'un autre utilisateur
    utilisateur = get_object_or_404(Utilisateur, id=user_id, is_active=True)
    forces = utilisateur.competences.filter(type_competence='force').select_related('competence')
    lacunes = utilisateur.competences.filter(type_competence='lacune').select_related('competence')
    disponibilites = utilisateur.disponibilites.all()

    contexte = {
        'utilisateur': utilisateur,
        'forces': forces,
        'lacunes': lacunes,
        'disponibilites': disponibilites,
    }
    return render(request, 'comptes/voir_profil.html', contexte)
