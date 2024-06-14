from users.models import Commentaire
from django import forms
from django.utils.translation import gettext_lazy as _

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        

        fields = ['content','parent']
        
        labels = {
            'content': _(''),
        }
        
        widgets = {
            'content' : forms.TextInput(),
        }