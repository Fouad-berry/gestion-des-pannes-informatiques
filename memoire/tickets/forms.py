from django import forms
from users.models import Ticket, Materiel


PRIORITES = (
    ("Faible", "Faible"),
    ("Normale", "Normale"),
    ("Elevée", "Elevée"),
)




class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        materiel = kwargs.pop('materiel', None)
        super().__init__(*args, **kwargs)
        if materiel:
            self.fields['materiel'].queryset = materiel
        

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ('plaignant', "reference",)

        widgets = {
            "materiel" : forms.Select(attrs={
                'class' : 'form-control form-select',
            }),
            "description" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "plaignant" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "reference" : forms.TextInput(attrs={
                'class' : 'form-control',
                'readonly': "readonly",
            }),
            "priorite" : forms.Select(attrs={
                'class' : 'form-control form-select',
            }),
            
        }
