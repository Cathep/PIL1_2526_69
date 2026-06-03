from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Utilisateur


class FormulaireInscription(forms.ModelForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label='Mot de passe'
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}),
        label='Confirmer le mot de passe'
    )

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Adresse email'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Numéro de téléphone'}),
        }

    def clean(self):
        donnees = super().clean()
        mdp = donnees.get('mot_de_passe')
        confirmer = donnees.get('confirmer_mot_de_passe')
        if not mdp or not confirmer:
            raise forms.ValidationError("Veuillez saisir et confirmer votre mot de passe.")
        if mdp != confirmer:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        validate_password(mdp)
        return donnees

    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        utilisateur.set_password(self.cleaned_data['mot_de_passe'])
        if commit:
            utilisateur.save()
        return utilisateur


class FormulaireConnexion(forms.Form):
    identifiant = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email ou téléphone'}),
        label='Email ou téléphone'
    )
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label='Mot de passe'
    )


class FormulaireResetPasswordDemande(forms.Form):
    identifiant = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email ou téléphone'}),
        label='Email ou téléphone'
    )


class FormulaireResetPassword(forms.Form):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau mot de passe'}),
        label='Mot de passe'
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}),
        label='Confirmer le mot de passe'
    )

    def clean(self):
        donnees = super().clean()
        mdp = donnees.get('mot_de_passe')
        confirmer = donnees.get('confirmer_mot_de_passe')
        if not mdp or not confirmer:
            raise forms.ValidationError("Veuillez saisir et confirmer votre mot de passe.")
        if mdp != confirmer:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        validate_password(mdp)
        return donnees


class FormulaireProfilBase(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'telephone', 'bio', 'photo_profil', 'filiere', 'niveau', 'role']


class FormulaireProfilCompetences(forms.Form):
    # formulaire vide - les competences sont gerees via POST lists
    pass
