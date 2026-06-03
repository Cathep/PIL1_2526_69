# IFRI_MentorLink

Application web de mentorat académique et professionnel pour les étudiants de l'IFRI.

Projet intégrateur 2025-2026 - Groupe 69  
Université d'Abomey-Calavi - Institut de Formation et de Recherche en Informatique

## Objectif

IFRI_MentorLink met en relation les étudiants qui souhaitent offrir ou recevoir du mentorat. L'application permet de créer un profil, publier des offres ou demandes de mentorat, lancer un algorithme de matching et échanger via une messagerie intégrée.

## Fonctionnalités

- Inscription, connexion et réinitialisation du mot de passe.
- Profil utilisateur avec filière, niveau, bio, photo, compétences, lacunes et disponibilités.
- Publication d'offres et de demandes de mentorat.
- Recherche de publications par type, compétence et jour.
- Matching mentor/mentoré selon les compétences, horaires, filière et niveau.
- Acceptation ou refus des suggestions de matching.
- Messagerie entre utilisateurs, avec support WebSocket via Django Channels.

## Technologies

- Backend : Python, Django
- Frontend : HTML, CSS, JavaScript
- Base de données : MySQL
- Temps réel : Django Channels

## Structure du projet

```text
mentorlink/
├── comptes/        # Authentification, profils, compétences, disponibilités
├── mentorat/       # Offres, demandes et matching
├── messagerie/     # Conversations et messages
├── mentorlink/     # Configuration Django
├── templates/      # Interfaces HTML
├── static/         # CSS et images
├── sql/            # Schémas SQL
└── docs/           # Rapport de projet
```

## Installation

Créer et activer un environnement virtuel :

```bash
python3 -m venv venv
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Configurer MySQL :

```sql
CREATE DATABASE mentorlink CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mentorlink_user'@'localhost' IDENTIFIED BY 'Mentorlink2025';
GRANT ALL PRIVILEGES ON mentorlink.* TO 'mentorlink_user'@'localhost';
FLUSH PRIVILEGES;
```

Appliquer les migrations :

```bash
python manage.py migrate
```

Créer un administrateur :

```bash
python manage.py createsuperuser
```

Lancer le serveur :

```bash
python manage.py runserver
```

Ouvrir ensuite :

```text
http://127.0.0.1:8000/
```

## Schéma SQL final

Le schéma final de la base de données est disponible ici :

```text
sql/schema_final.sql
```

## Rapport

Le rapport HTML du projet est disponible ici :

```text
docs/rapport.html
```

## Comptes et sécurité

- Les mots de passe sont hashés par le système d'authentification Django.
- L'accès aux pages principales est protégé par authentification.
- Les emails et numéros de téléphone sont uniques.
- Les conversations sont accessibles uniquement aux participants.

## GitHub

Dépôt du groupe :

```text
https://github.com/Cathep/PIL1_2526_69
```
