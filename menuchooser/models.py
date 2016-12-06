from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from menu.settings import BASE_DIR

#upload_location =FileSystemStorage(location=BASE_DIR+'/images/')
def get_user_image_folder(instance, filename):
    return "%s/images/%s" %(instance.owner.username, filename)

def get_tipo_folder(instance, filename):
    return "%s/images/%s" %(instance.Tipo, filename)

# Create your models here.
class TipoModel(models.Model):
    Tipo = models.CharField(max_length=30)
    Imagen= models.ImageField(upload_to=get_tipo_folder, blank=True)

    def __unicode__(self):
        return self.Tipo
class MenuModel(models.Model):

    Titulo = models.CharField(max_length=50)
    Ingredientes = models.TextField()
    Receta = models.TextField()
    Imagen= models.ImageField(upload_to=get_user_image_folder, blank=True)
    Imagen_URL= models.URLField(blank=True)
    pub_date= models.DateTimeField( auto_now=True)
    Tipo = models.ForeignKey(TipoModel, on_delete=models.PROTECT, default=1)
    publica = models.BooleanField( default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.Titulo

    def delete(self,*args,**kwargs):
        if self.Imagen:
            self.Imagen.delete()
        super(MenuModel, self).delete(*args,**kwargs)
