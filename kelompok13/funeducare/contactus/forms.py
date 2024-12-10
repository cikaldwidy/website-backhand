from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    contact = forms.CharField(label='Contact Number', max_length=20, required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, required=True)