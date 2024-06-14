from django import forms
from users.models import Direction, Ticket



class DirectionForm(forms.ModelForm):
    
    class Meta:
        model = Direction
        fields = "__all__"

        widgets = {
            "nom" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "code" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
        }
    


class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ("agent", 'date', 'plaignant', "reference")

        widgets = {
            "objet" : forms.Select(attrs={
                'class' : 'form-control',
            }),
            "description" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "agent" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "date" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "plaignant" : forms.EmailInput(attrs={
                'class' : 'form-control',
            }),
            "reference" : forms.TextInput(attrs={
                'class' : 'form-control',
                'readonly': "readonly",
            }),
        }
