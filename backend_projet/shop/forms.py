from django import forms
from .models import Pays, President

class PaysForm(forms.ModelForm):
    class Meta:
        model = Pays
        fields = ('nom', 'population')


class PresidentForm(forms.ModelForm):
    class Meta:
        model = President
        fields = ('nom', 'age', 'image', 'genre', 'pays')

