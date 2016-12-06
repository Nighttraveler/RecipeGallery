from django import forms
from pagedown.widgets import PagedownWidget
from models import MenuModel
from django.contrib.auth.models import User



class MenuForm(forms.ModelForm):
    Ingredientes = forms.CharField(widget=PagedownWidget())
    Receta = forms.CharField(widget=PagedownWidget())


    class Meta:
        model   = MenuModel
        fields  = [ 'Titulo','Tipo','publica','Imagen','Imagen_URL', 'Ingredientes', 'Receta','owner'  ]
        widgets = {
            'owner'     : forms.TextInput(attrs={'type':'hidden',
                                                })
        }



class UpdateProfile(forms.ModelForm):



    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

"""    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
"""
