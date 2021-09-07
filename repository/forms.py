from django import forms
from django.forms import widgets, HiddenInput
from .models import Repository


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = [
            'tags',
        ]
        widget=forms.Select(attrs={'onchange': 'submit();'})