from django import forms
from pagedown.widgets import PagedownWidget
from models import MenuModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MenuForm(forms.ModelForm):
    Ingredientes = forms.CharField(widget=PagedownWidget())
    Receta = forms.CharField(widget=PagedownWidget())


    class Meta:
        model   = MenuModel
        fields  = [ 'Titulo','Tipo','publica','Imagen','Imagen_URL', 'Ingredientes', 'Receta','owner'  ]
        widgets = {
            'Imagen_URL': forms.URLInput(attrs={'placeholder':'URL alternativa',
                                                'class':'form-control',
                                                }),
            'Titulo'    : forms.TextInput(attrs={'class':'form-control'}),
            'owner'     : forms.TextInput(attrs={'type':'hidden',
                                                })

        }


class myUserCreationForm(UserCreationForm):

    class Meta:
        model=User
        fields = ('username','email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
