from django import forms
from users.models import Direction, Employee
from django.utils.translation import gettext_lazy as _



POSTES = (
    ("Directeur", "Directeur"),
    ("Directeur Adjoint", "Directeur Adjoint"),
    ("Employé", "Employé"),
    ("Stagiaire", "Stagiaire"),
)
class EmployeeForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Identifiant'
            }), label="immatriculation")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Nom'
            }), label="Nom")
    first_name = forms.CharField(widget=forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Prénoms'
            }), label="Prenom")
    email = forms.CharField(widget=forms.EmailInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Email'
            }), max_length=255, required=False)
    password=forms.CharField(widget=forms.PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Mot de passe'
            }), label="Mot de passe", max_length=250, required=False)
    class Meta:
        model = Employee
        fields = ["bureau", "poste", "direction_employee", "adresse", "contact", "service_employee",]
        widgets = {
            "bureau" : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Bureau'
            }),
            "poste" : forms.Select(attrs={
                'class' : 'form-select',
                'placeholder' : 'Poste'
            }, choices=POSTES),
            "direction_employee": forms.Select(attrs={
                'class' : 'form-select',
                'placeholder' : 'Direction'
            }),
            "service_employee": forms.Select(attrs={
                'class' : 'form-select',
                'placeholder' : 'Service'
            }),
            "adresse" : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Adresse'
            }),
            "contact" : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Contact : 0022997656565'
            }),
        }   


class ContactForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Prenoms'
    }), label="Prenoms")

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Nom'
    }), label="Nom")

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Sujet'
    }), label="Sujet")

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Email'
    }), max_length=255, required=True,label='Email')

    content = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Entrez votre message ici'
    }), label="Contenu")