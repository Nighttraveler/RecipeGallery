from django.contrib import admin
from models import MenuModel, TipoModel
# Register your models here.

admin.site.register(MenuModel)
admin.site.register(TipoModel, admin_class=None)
