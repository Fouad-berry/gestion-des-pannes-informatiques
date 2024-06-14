# Generated by Django 4.1.7 on 2023-05-02 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code de la direction')),
                ('nom', models.CharField(max_length=255, unique=True, verbose_name='Nom de la direction')),
            ],
            options={
                'verbose_name': 'Direction',
                'verbose_name_plural': 'Directions',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bureau', models.CharField(max_length=50, verbose_name='Numero du bureau')),
                ('poste', models.CharField(default='employee', max_length=50, verbose_name='Poste')),
                ('contact', models.CharField(blank=True, max_length=50, null=True, verbose_name='Numero de telephone')),
                ('adresse', models.CharField(blank=True, max_length=50, null=True, verbose_name='Adresse')),
                ('direction_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.direction', verbose_name='Direction')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Materiel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, verbose_name='Nom')),
                ('marque', models.CharField(max_length=50, verbose_name='Marque')),
                ('modele', models.CharField(max_length=50, verbose_name='Modèle')),
                ('processeur', models.CharField(max_length=50, verbose_name='Processeur')),
                ('ram', models.CharField(max_length=50, verbose_name='RAM')),
                ('rom', models.CharField(max_length=50, verbose_name='ROM')),
                ('se', models.CharField(max_length=50, verbose_name="Systèmes d'Exploitations")),
                ('pack_office', models.CharField(max_length=50, verbose_name='Pack Office')),
                ('logicels_installes', models.CharField(max_length=50, verbose_name='Logiciels Installés')),
                ('antivrus', models.CharField(max_length=50, verbose_name='Solution Antivirus')),
                ('annee_nise_en_service', models.CharField(max_length=50, verbose_name='Année de mise en service')),
                ('etat_fonctionnement', models.CharField(max_length=50, verbose_name='Etat de fonctionnement')),
            ],
            options={
                'verbose_name': 'Materiel',
                'verbose_name_plural': 'Materiels',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=100, unique=True, verbose_name='Reference')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('priorite', models.CharField(choices=[('Faible', 'Faible'), ('Normale', 'Normale'), ('Elevée', 'Elevée')], max_length=11, verbose_name='Priorité du ticket :')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('materiel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.materiel', verbose_name='')),
                ('plaignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.employee', verbose_name='Employé')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
        migrations.CreateModel(
            name='Panne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.CharField(choices=[('en cours', 'En cours de traitement'), ('termine', 'Termine')], default='en cours', max_length=50, verbose_name='Etat')),
                ('observation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Obsservation')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.employee', verbose_name='Employe')),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.ticket', verbose_name='')),
            ],
            options={
                'verbose_name': 'Panne',
                'verbose_name_plural': 'Pannes',
            },
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Contenu')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.employee', verbose_name='')),
                ('panne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.panne', verbose_name='')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='users.commentaire')),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]