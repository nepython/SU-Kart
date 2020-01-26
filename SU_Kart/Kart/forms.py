from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import WebsiteUser

STATUS_CHOICES = (('Shopper', 'shopper'),
                  ('Delivery', 'delivery'))


class SignUpForm(forms.ModelForm):
    Task = forms.ChoiceField(choices=STATUS_CHOICES, required=True)

    class Meta:
        model = WebsiteUser
        fields = ('name', 'Email', 'DOB', 'UID', 'City', 'State', 'Task')

class SignInForm(forms.ModelForm):

    class Meta:
        model = WebsiteUser
        fields = ('name', 'DOB')


class ComplainForm(forms.ModelForm):

    class Meta:
        model = WebsiteUser
        fields = ('complain',)