from django import forms
from users.models import Materiel


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

class MaterielForm(forms.ModelForm):
   
    class Meta:
        model = Materiel
        fields = "__all__"
        widgets = {
            "nom" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "marque" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "modele": forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "annee_mise_en_service" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "etat_fonctionnement" : forms.Select(attrs={
                'class' : 'form-control',
            }, choices=ETAT_FONCTIONNEMENT),
            "image" : forms.FileInput(attrs={
                'class' : 'form-control',
            }),
            "type" : forms.Select(attrs={
                'class' : 'form-control form-select',
            }, choices=TYPES_MATERIELS),
            "utilisateur" : forms.Select(attrs={
                'class' : 'form-control form-select',
            }),
        }