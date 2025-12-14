from django import forms
from . models import Candidates

class Candidateapplyform(forms.ModelForm):
    class Meta:
        model=Candidates
        fields=['position',"manifesto"]