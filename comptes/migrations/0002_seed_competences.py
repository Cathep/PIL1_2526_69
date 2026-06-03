from django.db import migrations


def create_default_competences(apps, schema_editor):
    Competence = apps.get_model('comptes', 'Competence')
    default_competences = [
        {'nom': 'Programmation Python', 'categorie': 'Programmation'},
        {'nom': 'Programmation Java', 'categorie': 'Programmation'},
        {'nom': 'Développement Web', 'categorie': 'Web'},
        {'nom': 'Bases de données', 'categorie': 'Data'},
        {'nom': 'Intelligence artificielle', 'categorie': 'IA'},
        {'nom': 'Machine Learning', 'categorie': 'IA'},
        {'nom': 'Réseaux', 'categorie': 'Infrastructure'},
        {'nom': 'Sécurité informatique', 'categorie': 'Sécurité'},
        {'nom': 'Gestion de projet', 'categorie': 'Productivité'},
        {'nom': 'Communication', 'categorie': 'Soft skills'},
        {'nom': 'Analyse de données', 'categorie': 'Data'},
        {'nom': 'Développement mobile', 'categorie': 'Web'},
    ]
    for competence in default_competences:
        Competence.objects.get_or_create(
            nom=competence['nom'],
            defaults={'categorie': competence['categorie']},
        )


def delete_default_competences(apps, schema_editor):
    Competence = apps.get_model('comptes', 'Competence')
    noms = [
        'Programmation Python',
        'Programmation Java',
        'Développement Web',
        'Bases de données',
        'Intelligence artificielle',
        'Machine Learning',
        'Réseaux',
        'Sécurité informatique',
        'Gestion de projet',
        'Communication',
        'Analyse de données',
        'Développement mobile',
    ]
    Competence.objects.filter(nom__in=noms).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('comptes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_competences, delete_default_competences),
    ]
