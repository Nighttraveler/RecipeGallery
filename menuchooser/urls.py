from django.conf.urls import url
from . import views


app_name='menu'

urlpatterns = [
   url(r'^$', views.IndexFoodView.as_view(), name='index'),
   url(r'^agregar-receta/$', views.AddFoodView.as_view(), name='addfood'),
   url(r'^editar-receta/(?P<pk>[0-9]+)/$', views.EditFoodView.as_view() , name='editfood'),
   url(r'^delete/(?P<pk>\d+)/$', views.DeleteFoodView.as_view() , name='deletefood'),
   url(r'^(?P<pk>\d+)/$', views.TipoView.as_view(), name='tipofood'),
]
