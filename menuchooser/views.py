from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic, View
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from  models import MenuModel,TipoModel
from forms import MenuForm



# Create your views here.

class IndexFoodView(View):

    template_name = 'menuchooser/base.html'
    tipos= TipoModel.objects.all()
    form_class = MenuForm
    recetas= MenuModel.objects.all()
    query=None
    def buscar(self,r):
        if r.GET.get('q'):
            q=r.GET['q']
            self.query = q
            self.recetas= MenuModel.objects.filter(
                Q(Titulo__icontains=q)|
                Q(Ingredientes__icontains=q)|
                Q(Receta__icontains=q)
                )

    def filtrar_por(self,r):
        if r.GET.get('tipo'):
            tipo=r.GET['tipo']
            self.recetas = MenuModel.objects.filter(Tipo=tipo)


    def get(self, request):

        self.filtrar_por(request)
        self.buscar(request)

        per_page=8
        paginator = Paginator(self.recetas, per_page)
        page= request.GET.get('page')
        try:
            receta_pag = paginator.page(page)

        except PageNotAnInteger:
            receta_pag = paginator.page(1)

        except EmptyPage:
            receta_pag = paginator.page(paginator.num_pages)

        context = {'recetas':receta_pag,'tipos':self.tipos,'query':self.query,'form':self.form_class}

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
            return HttpResponseRedirect(reverse_lazy('menu:index'))

        return render(request, self.template_name, {'form': self.form_class})


class EditFoodView(generic.UpdateView):

    template_name = 'menuchooser/editar-receta.html'
    model = MenuModel
    form_class = MenuForm
    success_url = reverse_lazy('menu:index')




class DeleteFoodView(generic.DeleteView):

    context_object_name = 'receta'
    model = MenuModel
    template_name = 'menuchooser/borrar-receta.html'
    success_url = reverse_lazy('menu:index')
