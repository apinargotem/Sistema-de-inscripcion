
from decimal import Decimal
from gestión_académica.models import Curso


class Carrito:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = []
        self.carrito = carrito

    def agregar(self,producto):
        agrego = False
        ids = [car['producto_id'] for car in self.carrito]
        if not producto.Codigo in ids:
            self.carrito.append({
                "producto_id": producto.Codigo,
                "nombre": producto.Nombre,
                "acumulado": producto.Valor,
                "cantidad": 1,
            })
            self.guardar_carrito()
            agrego = True
        return agrego

        # self.carrito =
        # if id  not in self.carrito:
        #     self.carrito[id]={
        #         "producto_id": producto.Codigo,
        #         "nombre": producto.Nombre,
        #         "acumulado": producto.Valor,
        #         "cantidad": 1,
        #     }
        #
        # else:
        #     self.carrito[id]["cantidad"] += 1
        #     self.carrito[id]["acumulado"] += producto.Valor
        #self.guardar_carrito()

        #validación para no añadir dos veces el mismo curso
        #
        # if id==id in self.carrito.keys():
        #  del self.carrito[id]
        # else:
        #     id = str(producto.Codigo)
        # if id not in self.carrito.keys():
        #     self.carrito[id]={
        #         "producto_id": producto.Codigo,
        #         "nombre": producto.Nombre,
        #         "acumulado": producto.Valor,
        #         "cantidad": 1,
        #     }
         



    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True


    def eliminar(self, producto):
        self.carrito = [car for car in self.carrito if car['producto_id'] != producto.Codigo]
        self.guardar_carrito()


    def restar(self, producto):
        id = str(producto.Codigo)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= producto.Valor
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()


    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
       
    # def __iter__(self):
    #
    #     product_ids = [car['producto_id'] for car in self.carrito]
    #     products = Curso.objects.filter(Codigo__in=product_ids)
    #
    #     for producto in products:
    #         self.carrito['producto_id'] = producto
    #         self.carrito['acumulado'] = float(producto.Valor)
    #
    #     for item in self.carrito:
    #
    #         item['acumulado'] = float(item['acumulado'])
    #         item['total_precio'] = item['acumulado']
    #
    #         yield item

   
    def get_total_price(self):
        return sum(float(item['acumulado'])  for item in self.carrito.values())

       
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True