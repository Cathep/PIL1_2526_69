from django.db import models
from comptes.models import Disponibilite, Utilisateur, Competence


class DemandeOuOffre(models.Model):
    TYPES = [
        ('offre', 'Offre de mentorat'),
        ('demande', 'Demande de mentorat'),
    ]
    FORMATS = [
        ('presentiel', 'Présentiel'),
        ('en_ligne', 'En ligne'),
        ('les_deux', 'Les deux'),
    ]
    STATUTS = [
        ('ouvert', 'Ouvert'),
        ('matche', 'Matché'),
        ('ferme', 'Fermé'),
    ]

    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='publications')
    type_publication = models.CharField(max_length=10, choices=TYPES)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    format_seance = models.CharField(max_length=15, choices=FORMATS, default='les_deux')
    jour = models.CharField(max_length=10, choices=Disponibilite.JOURS, blank=True, null=True)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=10, choices=STATUTS, default='ouvert')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentoring_requests'
        verbose_name = 'Offre/Demande'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.type_publication} - {self.competence} par {self.auteur}"


class Matching(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]

    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchings_mentor')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchings_mentore')
    score_global = models.DecimalField(max_digits=5, decimal_places=2)
    score_competences = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score_horaires = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score_filiere = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    statut = models.CharField(max_length=15, choices=STATUTS, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'match_suggestions'
        unique_together = ('mentor', 'mentore')
        verbose_name = 'Matching'
        ordering = ['-score_global']

    def __str__(self):
        return f"Match {self.mentor} → {self.mentore} ({self.score_global}%)"

    def competences_communes(self):
        mentor_forces = set(self.mentor.competences.filter(type_competence='force').values_list('competence__nom', flat=True))
        mentore_lacunes = set(self.mentore.competences.filter(type_competence='lacune').values_list('competence__nom', flat=True))
        return sorted(mentor_forces & mentore_lacunes)

    def disponibilites_communes(self):
        result = []
        for dispo_mentor in self.mentor.disponibilites.all():
            for dispo_mentore in self.mentore.disponibilites.all():
                if dispo_mentor.jour != dispo_mentore.jour:
                    continue
                debut = max(dispo_mentor.heure_debut, dispo_mentore.heure_debut)
                fin = min(dispo_mentor.heure_fin, dispo_mentore.heure_fin)
                if debut < fin:
                    result.append(f"{dispo_mentor.get_jour_display()} {debut.strftime('%H:%M')} - {fin.strftime('%H:%M')}")
        return result
