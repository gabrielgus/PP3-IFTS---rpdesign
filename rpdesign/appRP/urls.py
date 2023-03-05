from django.urls import path
from . import views

app_name = 'appRP'

urlpatterns = [
    path('', views.index, name='inicio'),
    path('decoracion/', views.decoracion, name='decoracion'),
    path('<int:id>/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('contacto/', views.contacto, name='contacto'),

    path('login/', views.logueo, name='login'),
    path('logout/', views.deslogueo, name='logout'),

    path('alta_usuario/', views.alta_usuario, name='alta_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    
    path('alta_producto/', views.alta_producto, name='alta_producto'),
    path('edita_producto/<int:producto_id>/', views.edita_producto, name='edita_producto'),
    path('elimina_producto/<int:producto_id>', views.elimina_producto, name='elimina_producto'),
    path('productos/', views.productos, name='productos'),

    path('carrito/', views.carrito_detalle, name='carrito_detalle'),
    path('carrito/add/<int:producto_id>/', views.carrito_add, name='carrito_add'),
    path('carrito/remove/<int:producto_id>/', views.carrito_remove, name='carrito_remove'),

    path('crear/', views.crear_orden, name='crear_orden'),
    path('proceso_pago/', views.proceso_pago, name='proceso_pago'),
    path('orden_cancelada/<int:orden_id>', views.orden_cancelada, name='orden_cancelada'),
    path('completado/', views.pago_completado, name='completado'),
    path('cancelado/', views.pago_cancelado, name='cancelado'),

    path('error/', views.error, name='404'),
]