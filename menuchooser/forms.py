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
            'Imagen_URL': forms.URLInput(attrs={'placeholder':'URL alternativa',
                                                'class':'form-control',
                                                }),
            'Titulo'    : forms.TextInput(attrs={'class':'form-control'}),
            'owner'     : forms.TextInput(attrs={'type':'hidden',
                                                })

        }
