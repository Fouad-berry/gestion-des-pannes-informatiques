from django import forms
from users.models import Service


class ServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = "__all__"

        widgets = {
            "nom" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "code" : forms.TextInput(attrs={
                'class' : 'form-control',
            }),
            "direction_service" : forms.Select(
                attrs={
                    'class' : 'form-control',
                }
            )
        }
    