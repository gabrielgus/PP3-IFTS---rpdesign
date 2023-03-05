from decimal import Decimal
from django.conf import settings
from .models import Producto

class Carrito:
    def __init__(self, request):
        # Inicializa el carrito.
        self.session = request.session
        carrito = self.session.get(settings.CART_SESSION_ID)
        if not carrito:
            # guardo un carrito vacio en la sesión
            carrito = self.session[settings.CART_SESSION_ID] = {}
        self.carrito = carrito


    def add(self, producto, cantidad=1, anular_cantidad=False):
        # Agrego producto al carrito o actualizo su cantidad.
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {'cantidad': 0,
                                        'precio': str(producto.precio)}
        if anular_cantidad:
            self.carrito[producto_id]['cantidad'] = cantidad
        else:
            self.carrito[producto_id]['cantidad'] += cantidad
        self.save()


    def save(self):
        self.session.modified = True


    def remove(self, producto):
        # Elimino un producto del carrito.
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.save()


    def __iter__(self):
        producto_ids = self.carrito.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        carrito = self.carrito.copy()
        for producto in productos:
            carrito[str(producto.id)]['producto'] = producto
        for item in carrito.values():
            item['precio'] = Decimal(item['precio'])
            item['precio_total'] = item['precio'] * item['cantidad']
            yield item

    
    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())
    

    def get_precio_total(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())
    

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()