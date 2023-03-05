from django.contrib import admin

# Register your models here.
from appRP.models import Producto, Usuario, Orden, OrdenItem


admin.site.site_header = 'RP design'
admin.site.index_title = 'Panel de control de RP design'


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'dni', 'calle', 'altura', 'piso', 
                    'depto', 'localidad', 'cod_postal', 'is_staff', 'is_admin']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion',
                    'formato', 'precio', 'imagen', 'cantidad', 
                    'disponible', 'creado_el', 'slug']
    list_filter = ['disponible', 'creado_el']
    list_editable = ['precio', 'disponible']
    prepopulated_fields = {'slug': ('nombre',)}

class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    raw_id_fields = ['producto']
    
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'calle', 'altura', 'piso',
                     'depto', 'localidad', 'cod_postal', 'pagada', 'creada', 'actualizada']
    list_filter = ['pagada', 'creada', 'actualizada']
    inlines = [OrdenItemInline]