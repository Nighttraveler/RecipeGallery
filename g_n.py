# -*- coding: utf-8 -*-
from menuchooser.models import MenuModel,TipoModel
from django.contrib.auth.models import User
## REceta fernando panaderia
for i in range(1,15):
    m = MenuModel(
    Titulo="Receta"+str(i),
    Ingredientes= "Amasijo:    Harina 0000 500 grs    Sal 5 grs    Azúcar 15 grs    Levadura 30 grs Leche 250  Miel 15 grs Vainilla 1 cdta Empaste:    Manteca 200 grs    Harina 0000 25 grs    Doradura:    Yema c/n    Leche c/n    Opcional:Almíbar c/n    Miel c/n    Fiambres:    Jamón cocido   Jamón crudo    Lomito    Quesos:    De máquina Provolone     Reggianito     Cheddar",
    Receta= "Para el amasijo, hacer una corona con la harina y salar por el borde externo, En en centro, colocar la levadura, la miel, el azúcar, esencia y la leche de a poco a la vez que comenzamos a tomar la masa. Amasar por unos minutos y leudar al doble, tapada a temperatura ambiente.Para el empaste, mezclar la manteca con la harina.Para el armado, estirar el amasijo de manera rectangular y untar con el empaste. Cerrar y dar 3 vueltas simples (ver video) con 45 minutos de frío entre vuelta y vuelta.Para el armado, estirar y cortar triángulos de 15 cm de base. Enrollar estirando desde la punta y doblar los extremos sobre placa enmantecada.Pintar con la doradura (mezclar la leche con las yemas).Para la cocción, llevar al horno a 210 grados por 15 minutos y pintar con almíbar en caliente.Abrir al medio y rellenar con los fiambres y quesos a gusto. Gratinar.",
    Imagen_URL="http://www.cocinerosargentinos.com/images/3_Medialunas-de-manteca-rellenas-con-quesos-y-fiambres.jpg",
    Tipo=TipoModel.objects.get(Tipo="Panaderia"),
    owner=User.objects.get(username='capo')
    )
    if i%2==0:
        m.publica=True
    m.save()
    print('guardada receta'+str(i))

##Receta test1 plato
for i in range(1,15):
    m = MenuModel(
    Titulo="Receta"+str(i),
    Ingredientes= "Amasijo:    Harina 0000 500 grs    Sal 5 grs    Azúcar 15 grs    Levadura 30 grs Leche 250  Miel 15 grs Vainilla 1 cdta Empaste:    Manteca 200 grs    Harina 0000 25 grs    Doradura:    Yema c/n    Leche c/n    Opcional:Almíbar c/n    Miel c/n    Fiambres:    Jamón cocido   Jamón crudo    Lomito    Quesos:    De máquina Provolone     Reggianito     Cheddar",
    Receta= "Para el amasijo, hacer una corona con la harina y salar por el borde externo, En en centro, colocar la levadura, la miel, el azúcar, esencia y la leche de a poco a la vez que comenzamos a tomar la masa. Amasar por unos minutos y leudar al doble, tapada a temperatura ambiente.Para el empaste, mezclar la manteca con la harina.Para el armado, estirar el amasijo de manera rectangular y untar con el empaste. Cerrar y dar 3 vueltas simples (ver video) con 45 minutos de frío entre vuelta y vuelta.Para el armado, estirar y cortar triángulos de 15 cm de base. Enrollar estirando desde la punta y doblar los extremos sobre placa enmantecada.Pintar con la doradura (mezclar la leche con las yemas).Para la cocción, llevar al horno a 210 grados por 15 minutos y pintar con almíbar en caliente.Abrir al medio y rellenar con los fiambres y quesos a gusto. Gratinar.",
    Imagen_URL="http://www.cocinerosargentinos.com/images/1_Sandwiches-primaverales-de-entrana-y-vacio.jpg",
    Tipo=TipoModel.objects.get(Tipo="Platos"),
    owner=User.objects.get(username='administrador')
    )
    if i%2==0:
        m.publica=True
    m.save()
    print('guardada receta'+str(i))
