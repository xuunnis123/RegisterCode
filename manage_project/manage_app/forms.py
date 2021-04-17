
from django import forms
from django.core import validators
from manage_app.models import Code
class FormName(forms.Form):
    user=forms.CharField()
    code=forms.CharField()
    validate=forms.DateField()
    mac_address=forms.CharField()

class NewUserForm(forms.ModelForm):
    class Meta():
        model=Code

        fields='__all__'