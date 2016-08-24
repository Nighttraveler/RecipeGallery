from django import forms
from pagedown.widgets import PagedownWidget
from models import MenuModel

class MenuForm(forms.ModelForm):
    Ingredientes = forms.CharField(widget=PagedownWidget())
    Receta = forms.CharField(widget=PagedownWidget())


    class Meta:
        model = MenuModel
        fields = [ 'Titulo','Tipo','Imagen','Imagen_URL', 'Ingredientes', 'Receta'  ]
        widgets = {
            'Imagen_URL': forms.URLInput(attrs={'placeholder':'Solo ingrese una URL si no posee imagen local',
                                                'style':'width:50%',
                                                'class':'form-control',
                                                }),
            'Imagen': forms.ClearableFileInput(),

        }
