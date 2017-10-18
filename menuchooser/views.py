from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic, View
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Min, Sum, Avg

from  models import MenuModel,TipoModel,ProfileModel
from forms import MenuForm , ProfileForm, UserForm
from django.contrib.auth.models import User


##################################################################################################################
#Recipe views
##################################################################################################################


class HomePageView(generic.TemplateView):
    template_name = 'menuchooser/home.html'
    tipos = TipoModel.objects.all().exclude(pk=1)

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('menu:feed'))
        recetas_recientes = MenuModel.objects.filter(publica=True).order_by('-pub_date')[:5]
        context={'recetas_recientes':recetas_recientes,
                 'tipos':self.tipos}
        return render(request, self.template_name, context)

    def post(self, request):
        return self.get(request)


class IndexFeedView(generic.ListView):

    template_name = 'menuchooser/feed.html'
    tipos= TipoModel.objects.all()
    form_class = MenuForm
    model = MenuModel
    queryset = MenuModel.objects.all()
    query=None

    def buscar(self, qs, q ):
        return qs.filter(
            Q(Titulo__icontains=q) |
            Q(Ingredientes__icontains=q) |
            Q(Receta__icontains=q))

    def get_queryset(self, request):

        recetas = super(IndexFeedView, self).get_queryset()

        self.query = request.GET.get('q')

        if self.query:
            recetas = self.buscar(recetas, self.query)

        return recetas

    def paginate(self,recetas):
        per_page = 12
        paginator = Paginator(recetas.filter(publica=True).order_by('-pub_date'), per_page)
        page= self.request.GET.get('page')
        try:
            receta_pag = paginator.page(page)

        except PageNotAnInteger:
            receta_pag = paginator.page(1)

        except EmptyPage:
            receta_pag = paginator.page(paginator.num_pages)

        return receta_pag


    def get(self, request):

        recetas = self.get_queryset(request)

        receta_pag = self.paginate(recetas)

        context = {'recetas':receta_pag,'tipos':self.tipos,
                    'query':self.query,'form':self.form_class}

        return render(request, self.template_name, context)


class TipoView(IndexFeedView):

    recetas = None
    template_name = 'menuchooser/feed.html'

    def get(self,request,pk):
        tipo = get_object_or_404(TipoModel,pk=pk)
        self.recetas = MenuModel.objects.filter(Tipo=tipo)

        query = request.GET.get('q')
        if query:
            self.recetas = self.buscar(self.recetas, query)

        receta_pag = super(TipoView,self).paginate( self.recetas)

        context =  {'recetas':receta_pag,
                    'tipos':self.tipos,
                    'form':self.form_class}

        return render(request, self.template_name, context)


class AddFoodView(View):

    template_name = 'menuchooser/agregar-receta.html'
    form_class = MenuForm


    def get(self, request):
        context = {'form': self.form_class }
        return render(request, self.template_name,context)

    def post(self,request):
        f = self.form_class(request.POST, request.FILES)


        if f.is_valid():
            f.clean()
            f.save()
            return HttpResponseRedirect(reverse_lazy('menu:feed'))

        return render(request, self.template_name, {'form': self.form_class})


class EditFoodView(generic.UpdateView):

    template_name = 'menuchooser/editar-receta.html'
    model = MenuModel
    form_class = MenuForm
    success_url = reverse_lazy('menu:feed')

    def get_context_data(self, **kwargs):
        context = super(EditFoodView, self).get_context_data(**kwargs)
        if (context['object'].owner == self.request.user):
            #print('el usuario logueado es el dueno')
            context['owner'] = True

        return context


class DeleteFoodView(generic.DeleteView):

    context_object_name = 'receta'
    model = MenuModel
    template_name = 'menuchooser/borrar-receta.html'
    success_url = reverse_lazy('menu:feed')

class FoodDetailView(generic.DetailView):

    model = MenuModel

    template_name = 'menuchooser/detalle-receta.html'

    def get(self,request,pk ):
        receta = get_object_or_404(MenuModel, pk=pk)
        receta_id = receta.pk
        liked = False
        if request.session.get('has_liked_'+str(receta_id), liked):
            liked = True
            #print("liked {}_{}".format(liked, receta_id))
        context = {'receta':receta, 'liked': liked}
        return render(request ,self.template_name, context)


def like_count_recipe(request):
    liked = False
    if request.method == 'GET':
        recipe_id = request.GET['recipe_id']
        recipe = MenuModel.objects.get(id=int(recipe_id))
        if request.session.get('has_liked_'+recipe_id, liked):
            print("unlike")
            if recipe.likes > 0:
                likes = recipe.likes - 1
                try:
                    del request.session['has_liked_'+recipe_id]
                except KeyError:
                    print("keyerror")
        else:
            print("like")
            request.session['has_liked_'+recipe_id] = True
            likes = recipe.likes + 1
    recipe.likes = likes
    recipe.save()
    return HttpResponse(likes, liked)
#################################################################################################################
#USER views
#################################################################################################################

class UserProfileView(generic.DetailView, generic.FormView):
    model = User
    context_object_name = 'usuario'
    template_name = 'user/user-profile.html'
    form_class = MenuForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        #context['tipos'] = TipoModel.objects.all().order_by('-pk')
        context['tipos'] = TipoModel.objects.filter(
                                    menumodel__owner=kwargs['object']
                                    ).annotate(
                                    cant_recetas=Count('menumodel__Tipo')
                                    ).order_by('-pk')
        if context['tipos']:
            if (self.request.user==kwargs['object']):
                context['recetas'] = MenuModel.objects.filter(
                                        owner=kwargs['object']
                                        ).order_by('-pub_date')

                #print('privadas '+context['r'])
            else:
                context['recetas'] = MenuModel.objects.filter(
                                        owner=kwargs['object'],
                                        publica=True
                                        ).order_by('-pub_date')
                #print('publicas '+context['r'])


        return context


class UserEditView(View):

    user_form = None
    profile_form = None
    template_name = 'user/editar-usuario.html'

    def get(self, request, pk):
        self.user_form = UserForm(instance=request.user)
        self.profile_form = ProfileForm(instance=request.user.profilemodel)
        context = {
                'user_form': self.user_form,
                'profile_form': self.profile_form
                }
        return render(request, self.template_name ,context)

    def post(self, request ,pk):
        self.user_form = UserForm(request.POST, instance=request.user)
        self.profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profilemodel)


        if self.user_form.is_valid() and self.profile_form.is_valid():
            self.user_form.save()
            self.profile_form.save()

            return HttpResponseRedirect(reverse('menu:userprofile',kwargs={'pk':str(request.user.pk)}))

        self.user_form = UserForm(instance=request.user)
        self.profile_form = ProfileForm(instance=request.user.profilemodel)
        context = {
                'user_form': self.user_form,
                'profile_form': self.profile_form
                }

        return render(request, self.template_name)



    def get_success_url(self):
        return reverse('menu:userprofile',kwargs={'pk':str(self.object.pk)})

class SignUpView(generic.CreateView):
    template_name ='user/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
