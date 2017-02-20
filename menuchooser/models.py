from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_user_image_folder(instance, filename):
    return "%s/images/%s" % (instance.owner.username, filename)


def get_tipo_folder(instance, filename):
    return "%s/images/%s" % (instance.Tipo, filename)


def get_user_folder(instance, filename):
    return "%s/avatar/%s" % (instance.user.username, filename)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profilemodel.save()

# Create your models here.


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to=get_user_folder, blank=True)

    def __unicode__(self):
        return self.user.username


class TipoModel(models.Model):
    Tipo = models.CharField(max_length=30)
    Imagen = models.ImageField(upload_to=get_tipo_folder, blank=True)

    def __unicode__(self):
        return self.Tipo


class MenuModel(models.Model):

    Titulo = models.CharField(max_length=50)
    Ingredientes = models.TextField()
    Receta = models.TextField()
    Imagen = models.ImageField(upload_to=get_user_image_folder, blank=True)
    Imagen_URL = models.URLField(blank=True)
    pub_date = models.DateTimeField(auto_now=True)
    Tipo = models.ForeignKey(TipoModel, on_delete=models.PROTECT, default=1)
    publica = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.Titulo

    def delete(self, *args, **kwargs):
        if self.Imagen:
            self.Imagen.delete()
        super(MenuModel, self).delete(*args, **kwargs)
