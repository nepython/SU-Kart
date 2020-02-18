from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import WebsiteUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.forms import extras
from django.forms.widgets import DateInput


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #first_name = forms.CharField()
    #last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username','email' ,'password1', 'password2']

STATUS_CHOICES = (('Shopper', 'shopper'),
                  ('Delivery', 'delivery'))


class SignUpForm(forms.ModelForm):
    Task = forms.ChoiceField(choices=STATUS_CHOICES, required=True)
    #DOB = forms.DateField(widget=extras.SelectDateWidget)

    class Meta:
        model = WebsiteUser
        fields = ('DOB', 'UID', 'City', 'State', 'Task')
        widgets = {
            'DOB': DateInput(attrs={'type': 'date'})
        }


# class SignInForm(forms.ModelForm):
#
#     class Meta:
#         model = WebsiteUser
#         fields = ('name', 'DOB')


class ComplainForm(forms.ModelForm):

    class Meta:
        model = WebsiteUser
        fields = ('complain',)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'email']