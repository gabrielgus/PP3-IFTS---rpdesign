from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Producto")
    descripcion = models.CharField(max_length=250)
    formato = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    imagen = models.ImageField(upload_to='imagenes/', height_field=None, width_field=None, max_length=250)
    cantidad = models.IntegerField(default=0, blank=False)
    disponible = models.BooleanField(default=False, help_text="1-mostrar,0-ocultar")
    creado_el = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, default='')

    def __str__(self):
        return f"{self.nombre}"
    
    def get_absolute_url(self):
        return reverse('appRP:producto_detalle',
                        args=[self.id, self.slug])


class Usuario(AbstractUser):
    dni = models.PositiveIntegerField(verbose_name="Nro. de Documento", unique=True, default=0, blank=False, null=False)
    calle = models.CharField(max_length=255, blank=True, default='')
    altura = models.IntegerField(blank=True, default=0)
    piso = models.CharField(max_length=5, blank=True)
    depto = models.CharField(max_length=255, blank=True, default='')
    localidad = models.CharField(max_length=255, blank=True, default='')
    cod_postal = models.CharField(verbose_name="Codigo Postal", max_length = 255, blank=True, default='')
    is_admin = models.BooleanField(
        verbose_name="Es Administrador?",
        default=False,
        help_text=('Designa si un usuario es Administrador del sitio.'),
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Orden(models.Model):
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    calle = models.CharField(max_length=250, blank=True, default='')
    altura = models.IntegerField(blank=True, default=0)
    piso = models.CharField(max_length=5, blank=True)
    depto = models.CharField(max_length=10, blank=True)
    localidad = models.CharField(max_length=255, blank=True)
    cod_postal = models.CharField(verbose_name="Codigo Postal", max_length = 10, blank=True, default='')
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)
    pagada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creada']
        indexes = [
                models.Index(fields=['-creada']),
        ]

    def __str__(self):
        return f'Orden {self.id}'

    def get_costo_total(self):
        return sum(item.get_costo() for item in self.items.all())


class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='orden_items', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_costo(self):
        return self.precio * self.cantidad