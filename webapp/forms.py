# forms.py

from django import forms

class URLForm(forms.Form):
    long = forms.URLField(label='Enter URL', max_length=200, widget=forms.URLInput(attrs={'placeholder': 'https://example.com'}))
    alias = forms.CharField(label='Enter custom alias', max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'example'}))
    

    
