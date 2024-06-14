from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from memoire.settings import EMAIL_HOST_USER
from django.core.exceptions import ValidationError

def validator_min_length(value):
    if len(value) <= 4:
        raise ValidationError(
            _("Il faut au minimum 4 caracteres")
        )

# Create your models here.
ETATS=(
    ("en cours", "En cours de traitement"),
    ("termine", "Termine")
)

PRIORITES = (
    ("Faible", "Faible"),
    ("Normale", "Normale"),
    ("Elevée", "Elevée"),
)

ETAT_FONCTIONNEMENT = (
    ("Bon", "Bon"),
    ("Tres bon", "Tres bon"),
    ("Normal", "Normal"),
    ("Defectueux", "Defectueux"),
)

TYPES_MATERIELS = (
    ("Routeurs", "Routeurs"),
    ("Imprimantes", "Imprimantes"),
    ("PC", "PC"),
    ("Desktop", "Desktop"),
    ("Routeurs", "Routeurs"),
    ("Scanners", "Scanners"),
)

POSTES = (
    ("Directeur", "Directeur"),
    ("Directeur Adjoint", "Directeur Adjoint"),
    ("Employé", "Employé"),
    ("Stagiaire", "Stagiaire"),
)


class Direction(models.Model):
    """Model definition for Direction."""

    # TODO: Define fields here
    code = models.CharField(_("Code de la direction"), max_length=50, unique=True)
    nom = models.CharField(_("Nom de la direction"), max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Direction."""

        verbose_name = 'Direction'
        verbose_name_plural = 'Directions'

    def __str__(self):
        """Unicode representation of Direction."""
        return self.nom


class Employee(models.Model):
    user=models.OneToOneField(User, verbose_name=_("Employee"), on_delete=models.CASCADE)
    direction_employee = models.ForeignKey(Direction, verbose_name=_("Direction"), on_delete=models.SET_NULL, null=True, blank=True)
    service_employee = models.ForeignKey("Service", verbose_name=_("Service"), on_delete=models.SET_NULL, null=True, blank=True)
    bureau = models.CharField(_("Numero du bureau"), max_length=50)
    poste = models.CharField(_("Poste"), choices=POSTES, max_length=50, default="Employé")
    contact = models.CharField(_("Numero de telephone"), max_length=50, null=True, blank=True)
    adresse = models.CharField(_("Adresse"), max_length=50, null=True, blank=True, validators=[validator_min_length])
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Unicode representation of Division."""
        return self.user.username 


class Materiel(models.Model):

    nom = models.CharField(_("Nom"), max_length=50, unique=True)
    marque = models.CharField(_("Marque"), max_length=50)
    modele = models.CharField(_("Modèle"), max_length=50)
    type = models.CharField(_("Type de Matériel"), max_length=50, null=True, blank=True)
    annee_mise_en_service = models.CharField(_("Année de mise en service"), max_length=4, default="2023", validators=[validator_min_length])
    etat_fonctionnement = models.CharField(_("Etat de fonctionnement"), max_length=50, choices=ETAT_FONCTIONNEMENT, default='Normal')
    image = models.FileField(_("Images"), upload_to="uploads/materiels", max_length=100, null=True, blank=True)
    utilisateur = models.ForeignKey(Employee, verbose_name=_("Employe"), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = _("Materiel")
        verbose_name_plural = _("Materiels")

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse("Materiel_detail", kwargs={"pk": self.pk})



class Ticket(models.Model):
    """Model definition for Ticket."""

    # TODO: Define fields here
    reference = models.CharField(_("Reference"), max_length=100, unique=True)
    plaignant = models.ForeignKey(Employee, verbose_name=_("Employé"), on_delete=models.CASCADE)
    materiel =models.ForeignKey(Materiel, verbose_name=_("Materiel"), on_delete=models.CASCADE)
    priorite = models.CharField(_("Priorité du ticket :"), max_length=11, choices=PRIORITES)
    description = models.TextField(_("Description"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Ticket."""

        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        """Unicode representation of Ticket."""
        return self.reference
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Validate model fields before saving
        super().save(*args, **kwargs)


class Panne(models.Model):
    """Model definition for Panne."""

    # TODO: Define fields here
    agent = models.ForeignKey(Employee, verbose_name=_("Employé"), on_delete=models.SET_NULL, null=True, blank=True)
    ticket=models.OneToOneField(Ticket, verbose_name=_(""), on_delete=models.CASCADE)
    etat = models.CharField(_("Etat"), max_length=50, choices=ETATS, default="en cours")
    observation = models.CharField(_("Observation"), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Panne."""

        verbose_name = 'Panne'
        verbose_name_plural = 'Pannes'

    def __str__(self):
        """Unicode representation of Panne."""
        return self.ticket.reference
    
    def save(self, *args, **kwargs):
        # Save the instance
        super().save(*args, **kwargs)

        # Create a notification after saving the instance
        # create_panne_notification(sender=Panne, instance=self, created=True)
    
@receiver(post_save, sender=Panne)
def create_panne_notification(sender, instance, created, **kwargs):      
    if created and instance.etat != "terminé":
        # Get the superuser
        superuser = User.objects.filter(is_superuser=True).first()
        
        # Vérifier si un agent est assigné à la panne
        if instance.agent:
            # Envoyer un e-mail à l'agent assigné
            subject = f'Nouvelle panne assignée : {instance.ticket.reference}'
            message = f'Cher {instance.agent},\n\nUne nouvelle panne vous a été assignée. Veuillez prendre les mesures nécessaires.\n\nCordialement,\nVotre équipe de support'
            send_mail(subject, message, EMAIL_HOST_USER, [instance.agent.user.email])

        if superuser:
            # Create a notification for the superuser
            message = f"""Nouvelle panne ajoutée: {instance}\r\n\r\n\r\n\r\n
            Cher administrateur, l'utilisateur {instance.ticket.plaignant.user.username} vient de conster une panne sur le materiel {instance.ticket.materiel.nom}\r\n\r\n
            Description du ticket: {instance.ticket.description}.\r\n\r\n
            Merci de d'essayer d'y trouver une solution.
            """
            notification = Notification.objects.create(
                message=message,
                recipient=superuser,
                sender=instance.agent.user if instance.agent else None
            )
            send_mail(f'Notification Nouvelle panne {instance}', message, EMAIL_HOST_USER, [superuser.email])
        
    # Exclure l'envoi de notification lorsque l'instance est mise à jour pour ajouter un agent ou un commentaire
    if not created and not isinstance(instance.agent, models.Model) and not isinstance(instance.observation, models.Model):
        return
    # Reste du code pour créer la notification et envoyer un e-mail pour l'ajout d'un agent ou un commentaire
    # ...



class Commentaire(models.Model):
    panne=models.ForeignKey(Panne, verbose_name=_(""), on_delete=models.CASCADE)
    content=models.TextField(_("Contenu"))
    employee=models.ForeignKey(Employee, verbose_name=_(""), on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Commentaire.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class Notification(models.Model):
    message = models.CharField(max_length=255)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


class Service(models.Model):
    '''Model definition for Service.'''

    code  = models.CharField(_("Code du Service"), max_length=50, unique=True)
    nom = models.CharField(_("Nom du Service"), max_length=80)
    direction_service = models.ForeignKey(Direction, verbose_name=_("Direction du service"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''Meta definition for Service.'''

        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return "{}".format(self.nom)
    

class Contact(models.Model):

    '''Model definition for Contact.'''
    user = models.ForeignKey(User, verbose_name=_("Employe"), on_delete=models.SET_NULL, null=True, blank=True)
    email = models.CharField(verbose_name=_("Email"), max_length=120)
    subject = models.CharField(verbose_name=_("Sujet"), max_length=255)
    content = models.TextField(verbose_name=_("Contenu"))
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''Meta definition for Contact.'''

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


