from django import forms
from urlshortener.models import URLModel


class URLForm(forms.ModelForm):
    class Meta:
        model = URLModel
        fields = '__all__'
        error_messages = {
            'alias': {
                'unique': 'Thia Alias is associated with another URL.'
                          'Please try another Alias or leave it to be automatically generated.'
            }
        }
