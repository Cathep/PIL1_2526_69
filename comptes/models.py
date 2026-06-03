from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'fields_of_study'
        verbose_name = 'Filière'
        verbose_name_plural = 'Filières'

    def __str__(self):
        return self.nom


class Competence(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    categorie = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'skills'
        verbose_name = 'Compétence'

    def __str__(self):
        return self.nom


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, mot_de_passe=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, mot_de_passe, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('mentor', 'Mentor'),
        ('mentore', 'Mentoré'),
        ('les_deux', 'Les deux'),
    ]
    NIVEAUX = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    photo_profil = models.ImageField(upload_to='photos_profil/', blank=True, null=True)
    bio = models.TextField(blank=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.CharField(max_length=10, choices=NIVEAUX, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='les_deux')
    est_actif = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    token_reinitialisation = models.CharField(max_length=255, blank=True, null=True)
    token_expire_le = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']

    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class CompetenceUtilisateur(models.Model):
    TYPES = [
        ('force', 'Point fort'),
        ('lacune', 'Lacune'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='competences')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    type_competence = models.CharField(max_length=10, choices=TYPES)
    niveau = models.PositiveSmallIntegerField(default=3)  # niveau 1 a 5

    class Meta:
        db_table = 'user_skills'
        unique_together = ('utilisateur', 'competence', 'type_competence')
        verbose_name = 'Compétence utilisateur'

    def __str__(self):
        return f"{self.utilisateur} - {self.competence} ({self.type_competence})"


class Disponibilite(models.Model):
    JOURS = [
        ('Monday', 'Lundi'),
        ('Tuesday', 'Mardi'),
        ('Wednesday', 'Mercredi'),
        ('Thursday', 'Jeudi'),
        ('Friday', 'Vendredi'),
        ('Saturday', 'Samedi'),
        ('Sunday', 'Dimanche'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='disponibilites')
    jour = models.CharField(max_length=10, choices=JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        db_table = 'user_availabilities'
        verbose_name = 'Disponibilité'

    def __str__(self):
        return f"{self.utilisateur} - {self.jour} {self.heure_debut}-{self.heure_fin}"
