from django import forms


class SectionForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(required=True,
                              widget=forms.Textarea(attrs={'rows': '8', 'cols': '30'}))
