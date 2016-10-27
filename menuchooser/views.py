from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic, View
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserChangeForm


from  models import MenuModel,TipoModel
from forms import MenuForm, myUserCreationForm



# Create your views here.

class HomePageView(generic.TemplateView):
    recetas_recientes = MenuModel.objects.all().order_by('-pub_date')[:5]
    template_name = 'menuchooser/home.html'

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('menu:feed'))
        context={'recetas_recientes':self.recetas_recientes}
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

    def get(self, request):

        recetas = self.get_queryset(request)

        per_page = 24
        paginator = Paginator(recetas.order_by('-pub_date'), per_page)
        page= request.GET.get('page')
        try:
            receta_pag = paginator.page(page)

        except PageNotAnInteger:
            receta_pag = paginator.page(1)

        except EmptyPage:
            receta_pag = paginator.page(paginator.num_pages)

        context = {'recetas':receta_pag,'tipos':self.tipos,'query':self.query,'form':self.form_class}

        return render(request, self.template_name, context)


class TipoView(View):

    tipos = TipoModel.objects.all()
    recetas = None
    template_name = 'menuchooser/feed.html'
    form_class = MenuForm

    def buscar(self, qs, q ):
        return qs.filter(
            Q(Titulo__icontains=q) |
            Q(Ingredientes__icontains=q) |
            Q(Receta__icontains=q))


    def get(self,request,pk):
        tipo = get_object_or_404(TipoModel,pk=pk)
        self.recetas = MenuModel.objects.filter(Tipo=tipo)

        query = request.GET.get('q')
        if query:
            self.recetas = self.buscar(self.recetas, query)

        per_page =28
        paginator = Paginator(self.recetas.order_by('-pub_date'), per_page)
        page = request.GET.get('page')
        try:
            receta_pag = paginator.page(page)

        except PageNotAnInteger:
            receta_pag = paginator.page(1)

        except EmptyPage:
            receta_pag = paginator.page(paginator.num_pages)

        context =  {'recetas':receta_pag, 'tipos':self.tipos,'form':self.form_class}

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


class DeleteFoodView(generic.DeleteView):

    context_object_name = 'receta'
    model = MenuModel
    template_name = 'menuchooser/borrar-receta.html'
    success_url = reverse_lazy('menu:feed')

class FoodDetailView(generic.DetailView):

    model = MenuModel
    context_object_name = 'receta'
    template_name = 'menuchooser/detalle-receta.html'



### USER views
class UserProfileView(generic.DetailView):
    model = User
    context_object_name = 'usuario'
    template_name = 'user/user-profile.html'
    



class SignUpView(generic.CreateView):
    template_name ='user/registration.html'
    form_class = myUserCreationForm

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.clean()
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse_lazy('menu:index'))

        return render(request, self.template_name, {'form':self.form_class})
