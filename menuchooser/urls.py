from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from . import views
from . import forms


app_name ='menu'

urlpatterns = [

    url(r'^like-recipe/$', views.like_count_recipe, name='like_count_recipe'),
    ###USER ADMINISTRATION
    url(r'^accounts/register/$', views.SignUpView.as_view(), name="register"),


    url(r'^accounts/profile/(?P<pk>\d+)/$',
        login_required(views.UserProfileView.as_view()),
        name='userprofile'),

    url(r'^accounts/edituserprofile/(?P<pk>[0-9]+)/$',
        views.UserEditView.as_view(),
        name='edituserprofile'),


    url(r'^dashboard/$',views.IndexFeedView.as_view(), name='feed' ),

    #por alguna razon va despues de lo logout etc
    #rl(r'^accounts/', include('django.contrib.auth.urls')),

    # HOME
    url(r'^$', views.HomePageView.as_view(), name='index'),

    ## RECETAS
    url(r'^receta/(?P<pk>\d+)/detalle/$',
        views.FoodDetailView.as_view(),
         name='detailfood'),

    url(r'^categoria/(?P<pk>\d+)/$',
        views.TipoView.as_view(),
        name='tipofood'),

    url(r'^agregar-receta/$',
        views.AddFoodView.as_view(),
        name='addfood'),

    url(r'^editar-receta/(?P<pk>[0-9]+)/$',
        login_required(views.EditFoodView.as_view()) ,
        name='editfood'),

    url(r'^delete/(?P<pk>\d+)/$',
        views.DeleteFoodView.as_view() ,
        name='deletefood'),



]
