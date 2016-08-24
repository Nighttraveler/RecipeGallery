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
    recetas= None
    query=None

    def get(self, request):
        if request.GET.get('q'):
            q=request.GET['q']
            self.query = q
            self.recetas= MenuModel.objects.filter(
                Q(Titulo__icontains=q)|
                Q(Ingredientes__icontains=q)|
                Q(Receta__icontains=q)
                )
        else:
            self.recetas=MenuModel.objects.all().order_by('-pub_date')

        per_page=12
        paginator = Paginator(self.recetas, per_page)
        page= request.GET.get('page')

        try:
            receta_pag = paginator.page(page)

        except PageNotAnInteger:
            receta_pag = paginator.page(1)

        except EmptyPage:
            receta_pag = paginator.page(paginator.num_pages)

        context = {'recetas':receta_pag,'tipos':self.tipos,'query':self.query}

        return render(request, self.template_name, context)

class TipoView(View):

    tipos = TipoModel.objects.all()
    recetas = None
    template_name = 'menuchooser/base.html'

    def get(self,request,pk):
        tipo= get_object_or_404(TipoModel,pk=pk)
        self.recetas = MenuModel.objects.filter(Tipo=tipo)

        context=  {'recetas':self.recetas, 'tipos':self.tipos}

        return render(request, self.template_name, context)


class AddFoodView(View):

    template_name = 'menuchooser/agregar-receta.html'
    form_class = MenuForm
    tipos= TipoModel.objects.all()

    def get(self, request):
        context = {'form': self.form_class , 'tipos':self.tipos}
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
