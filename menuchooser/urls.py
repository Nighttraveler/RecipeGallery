from django.conf.urls import url
from . import views


app_name='menu'

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^users/$', views.IndexFeedView.as_view(), name='users'),
    url(r'^receta/(?P<pk>\d+)/detalle/$', views.FoodDetailView.as_view(), name='detailfood'),
    url(r'^categoria/(?P<pk>\d+)/$', views.TipoView.as_view(), name='tipofood'),
    url(r'^agregar-receta/$', views.AddFoodView.as_view(), name='addfood'),
    url(r'^editar-receta/(?P<pk>[0-9]+)/$', views.EditFoodView.as_view() , name='editfood'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteFoodView.as_view() , name='deletefood'),

]
