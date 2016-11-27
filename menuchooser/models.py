from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from menu.settings import BASE_DIR

upload_location =FileSystemStorage(location=BASE_DIR+'/images/')

# Create your models here.
class TipoModel(models.Model):
    Tipo = models.CharField(max_length=30)

    def __unicode__(self):
        return self.Tipo
class MenuModel(models.Model):

    Titulo = models.CharField(max_length=50)
    Ingredientes = models.TextField()
    Receta = models.TextField()
    Imagen= models.ImageField(upload_to=upload_location, blank=True)
    Imagen_URL= models.URLField(blank=True)
    pub_date= models.DateTimeField( auto_now=True)
    Tipo = models.ForeignKey(TipoModel, on_delete=models.CASCADE, default=1)
    publica = models.BooleanField( default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.Titulo

    def delete(self,*args,**kwargs):
        if self.Imagen:
            self.Imagen.delete()
        super(MenuModel, self).delete(*args,**kwargs)
