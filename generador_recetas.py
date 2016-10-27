from menuchooser.models import MenuModel

for i in range(0,50):
    r = MenuModel(
        Titulo="receta "+str(i),
        Ingredientes="Ingrediente "+str(i),
        Receta="Receta "+str(i),
        Imagen_URL="http://i.imgur.com/BniYvjG.jpg",
    )
    r.save()
    print ("Generando receta "+str(r.Titulo))
