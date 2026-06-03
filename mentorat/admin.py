from django.contrib import admin
from .models import DemandeOuOffre, Matching


@admin.register(DemandeOuOffre)
class DemandeOuOffreAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'type_publication', 'competence', 'format_seance', 'statut', 'date_creation')
    list_filter = ('type_publication', 'statut', 'format_seance')
    search_fields = ('auteur__nom', 'auteur__prenom', 'competence__nom')
    ordering = ('-date_creation',)


@admin.register(Matching)
class MatchingAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'mentore', 'score_global', 'score_competences', 'score_horaires', 'score_filiere', 'statut')
    list_filter = ('statut',)
    search_fields = ('mentor__nom', 'mentore__nom')
    ordering = ('-score_global',)
