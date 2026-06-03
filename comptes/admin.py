from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Filiere, Competence, CompetenceUtilisateur, Disponibilite


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie')
    list_filter = ('categorie',)
    search_fields = ('nom',)


class CompetenceUtilisateurInline(admin.TabularInline):
    model = CompetenceUtilisateur
    extra = 1


class DisponibiliteInline(admin.TabularInline):
    model = Disponibilite
    extra = 1


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('email', 'nom', 'prenom', 'telephone', 'filiere', 'niveau', 'role', 'is_active')
    list_filter = ('role', 'filiere', 'niveau', 'is_active')
    search_fields = ('email', 'nom', 'prenom', 'telephone')
    ordering = ('-date_inscription',)
    inlines = [CompetenceUtilisateurInline, DisponibiliteInline]

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('email', 'password', 'nom', 'prenom', 'telephone', 'photo_profil', 'bio')
        }),
        ('Infos académiques', {
            'fields': ('filiere', 'niveau', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'telephone', 'password1', 'password2'),
        }),
    )
