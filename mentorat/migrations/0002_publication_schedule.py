from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandeouoffre',
            name='jour',
            field=models.CharField(blank=True, null=True, choices=[
                ('Monday', 'Lundi'),
                ('Tuesday', 'Mardi'),
                ('Wednesday', 'Mercredi'),
                ('Thursday', 'Jeudi'),
                ('Friday', 'Vendredi'),
                ('Saturday', 'Samedi'),
                ('Sunday', 'Dimanche'),
            ], max_length=10),
        ),
        migrations.AddField(
            model_name='demandeouoffre',
            name='heure_debut',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='demandeouoffre',
            name='heure_fin',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
