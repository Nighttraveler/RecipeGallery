from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic, View
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from  models import MenuModel,TipoModel
from forms import MenuForm



# Create your views here.

class HomePageView(generic.TemplateView):
    recetas_recientes = MenuModel.objects.all().order_by('-pub_date')[:5]
    template_name = 'menuchooser/home.html'

    def get(self,request):
        context={'recetas_recientes':self.recetas_recientes}
        return render(request, self.template_name, context)


class IndexFeedView(generic.ListView):

    template_name = 'menuchooser/base.html'
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

        query = request.GET.get('q')

        if query:
            recetas = self.buscar(recetas, query)

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
    template_name = 'menuchooser/base.html'
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
            return HttpResponseRedirect(reverse_lazy('menu:users'))

        return render(request, self.template_name, {'form': self.form_class})


class EditFoodView(generic.UpdateView):

    template_name = 'menuchooser/editar-receta.html'
    model = MenuModel
    form_class = MenuForm
    success_url = reverse_lazy('menu:users')


class DeleteFoodView(generic.DeleteView):

    context_object_name = 'receta'
    model = MenuModel
    template_name = 'menuchooser/borrar-receta.html'
    success_url = reverse_lazy('menu:users')

class FoodDetailView(generic.DetailView):
    model = MenuModel
    context_object_name = 'receta'
    template_name = 'menuchooser/detalle-receta.html'

    def get_context_data(self, **kargs):
        context = super(FoodDetailView, self).get_context_data(**kargs)
        return context
