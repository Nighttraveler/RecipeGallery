from django import forms
from pagedown.widgets import PagedownWidget
from models import MenuModel, ProfileModel
from django.contrib.auth.models import User



class MenuForm(forms.ModelForm):
    Ingredientes = forms.CharField(widget=PagedownWidget())
    Receta = forms.CharField(widget=PagedownWidget())

    class Meta:
        model   = MenuModel
        fields  = [ 'Titulo','Tipo','publica','Imagen','Imagen_URL', 'Ingredientes', 'Receta','owner'  ]
        widgets = {
            'owner'     : forms.TextInput(attrs={'type':'hidden'})
        }




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')



class ProfileForm(forms.ModelForm):

    class Meta:
        model = ProfileModel
        fields = ['avatar','bio']
