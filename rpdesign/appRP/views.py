from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives

from appRP.models import Producto, Usuario, OrdenItem, Orden
from appRP.carrito import Carrito
from appRP.forms import AltaProducto, AltaUsuario, ModificaUsuario, CarritoAgregaProducto, CrearOrdenForm
from django.contrib import messages

from django.views.decorators.http import require_POST

from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import mercadopago

# Create your views here.

def index(request):
    context = {'barra': 'nav'}
    return render(request,'appRP/publica/index.html', context)

def decoracion(request):
    # ordenados de manera descendente
    # productos = Producto.objects.all().order_by('-id')
    # ordenados de manera ascendente(por defecto) 
    # productos = Producto.objects.all().order_by('id')
    productos = Producto.objects.filter(disponible=True).order_by('id')
    context = {'barra': 'nav2', 'lalista': productos}
    return render(request, 'appRP/publica/decor.html', context,)

def producto_detalle(request, id, slug):
    producto = get_object_or_404(Producto, id=id, slug=slug, disponible=True)
    carrito_producto_form = CarritoAgregaProducto()
    context = {'barra': 'nav2', 'producto': producto, 'carrito_producto_form': carrito_producto_form}
    return render(request, 'appRP/publica/detalle.html', context)

def contacto(request):
    context = {'barra': 'nav2'}
    return render(request,'appRP/publica/contact.html', context)

def logueo(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
            # Password correcto, y usuario marcado como "active"
                request.user = user
                login(request, user)
            # Redirecciono a la galeria
                return redirect("/decoracion")
            else:
            # Muestro un mensaje de error
                form = AuthenticationForm()
                messages.error(request, 'Se ha producido un error al autenticarse, Nombre de usuario ó Contraseña incorrectos')          
                return redirect("/login")
        else:
            form = AuthenticationForm()
    return render(request,'appRP/publica/login.html', {'form': form})

def deslogueo(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Se ha deslogueado correctamente")
  return redirect("/login")

@require_POST
def carrito_add(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    form = CarritoAgregaProducto(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        carrito.add(producto=producto,
                    cantidad=cd['cantidad'],
                    anular_cantidad=cd['anular'])
    return redirect('appRP:carrito_detalle')

@require_POST
def carrito_remove(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.remove(producto)
    return redirect('appRP:carrito_detalle')

@login_required(login_url=settings.LOGIN_URL)
def carrito_detalle(request):
    if request.user.is_authenticated:
        carrito = Carrito(request)
        for item in carrito:
            item['actualizar_cantidad_form'] = CarritoAgregaProducto(initial={
                                                                    'cantidad': item['cantidad'],
                                                                    'anular': True})
        return render(request, 'appRP/publica/carrito.html', {'carrito': carrito})
    else:
        return redirect('appRP:404')
    
@login_required(login_url=settings.LOGIN_URL)
def crear_orden(request):
    if request.user.is_authenticated:
        carrito = Carrito(request)
        if request.method == 'POST':
            form = CrearOrdenForm(request.POST)
            if form.is_valid():
                orden = form.save()
                for item in carrito:
                    OrdenItem.objects.create(orden=orden,
                                            producto=item['producto'],
                                            precio=item['precio'],
                                            cantidad=item['cantidad'])
                # Vacio el carrito
                carrito.clear()
                # almaceno la orden en la sesion
                request.session['orden_id'] = orden.id
            # redirecciono para pagar
            return redirect(reverse('appRP:proceso_pago'))
        else:
            envio = 1500.00
            usuario = Usuario.objects.get(id=request.user.id)
            form = CrearOrdenForm(instance=usuario)
        return render(request,'appRP/publica/crear.html', {'carrito': carrito, 'form': form , 'envio': envio})
    else:
        return redirect('appRP:404')

@login_required(login_url=settings.LOGIN_URL)
def proceso_pago(request):
    if request.user.is_authenticated:
        sdk = mercadopago.SDK(settings.ACCESS_TOKEN)
        orden_id = request.session.get('orden_id', None)
        orden = get_object_or_404(Orden, id=orden_id)
        exito_url = request.build_absolute_uri(reverse('appRP:completado'))
        fallo_url = request.build_absolute_uri(reverse('appRP:cancelado'))
        # Creo los datos de la preferencia
        preference_data = {
                    "back_urls": 
                        {
                    'failure': fallo_url, 
                    'pending': '', 
                    'success': exito_url,
                        },
                    'auto_return': 'approved',
                    'binary_mode': True,
                    'external_reference': orden.id,
                    'items': [{
                                'title': 'envio',
                                'quantity': 1,
                                'unit_price': float(1500.00),
                                'currency_id': 'ARS',
                                'description': 'Costo de envio',
                                        }],
                    "payment_methods": {
                            "excluded_payment_types": [
                                {
                                    "id": "ticket"
                                }
                            ],
                            "installments": 3
                        },
        }
        # agregar items de la orden
        for dato in orden.items.all():
            preference_data['items'].append({
                                    'title': dato.producto.nombre,
                                    'quantity': dato.cantidad,
                                    'unit_price': float(dato.precio),
                                    'currency_id': 'ARS',
                                    'description': dato.producto.nombre,
                                            })
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        id = preference["id"]
        envio = 1500.00
        return render(request, 'appRP/publica/proceso_pago.html', locals())
    else:
        return redirect('appRP:404')

@login_required(login_url=settings.LOGIN_URL)
def pago_completado(request):
    collection_status = request.GET['collection_status']
    external_reference = request.GET['external_reference']
    envio = {'title': 'envio',
            'quantity': 1,
            'unit_price': float(1500.00),
            'currency_id': 'ARS',
            'description': 'Costo de envio',}
    if collection_status == 'approved':
        try:
            orden = Orden.objects.get(id=request.GET['external_reference'])
        except Orden.DoesNotExist:
            return redirect('appRP:404')
        # marco la orden como pagada
        orden.pagada = True
        orden.save() 
        # genero la info para el mail
        data = {
            'items':[],
            }
        for dato in orden.items.all():
            data['items'].append({
                                'title': dato.producto.nombre,
                                'quantity': dato.cantidad,
                                'unit_price': float(dato.precio),
                                'currency_id': 'ARS',
                                'description': dato.producto.nombre,
                                        })
        subject = f'Orden de compra Nro. {orden.pk}'
        template = loader.get_template('appRP/publica/correo.html')
        content = template.render({
            'orden':orden, 
            'envio':envio,
        })
        message = EmailMultiAlternatives(subject, #Titulo
                                        content,
                                        settings.EMAIL_HOST_USER, #Remitente
                                        [settings.RECIPIENT_ADDRESS, orden.email],#Destinatario
                                        )                                            
        message.attach_alternative(content, 'text/html')
        message.send() 
    return render(request, 'appRP/publica/completado.html', {'collection_status': collection_status,
                                                             'external_reference': external_reference, 
                                                             'orden':orden, 
                                                             'envio':envio })

@login_required(login_url=settings.LOGIN_URL)
def pago_cancelado(request):
    return render(request, 'appRP/publica/cancelado.html')

@login_required(login_url=settings.LOGIN_URL)
def orden_cancelada(request, orden_id):
    if request.user.is_authenticated:
        orden = get_object_or_404(Orden, id=orden_id)
        orden.delete()
        return redirect('appRP:decoracion')
    else:
        return redirect('appRP:404')

def alta_usuario(request):
    context = {'barra': 'nav2'}
    if(request.method == 'POST'):
        altau_form = AltaUsuario(request.POST)
        if(altau_form.is_valid()):
            altau_form.save()
            messages.success(request,'Se ha creado al usuario correctamente')          
            return redirect('/login')
        else:
            messages.warning(request,'Por favor revisa los errores')
            return render(request,'appRP/publica/alta_usuario.html', {'context':context, 'altau_form':altau_form})
    else:
        altau_form = AltaUsuario()
        context = {'barra': 'nav'}
    return render(request,'appRP/publica/alta_usuario.html', {'context':context, 'altau_form':altau_form})

@login_required(login_url=settings.LOGIN_URL)
def editar_usuario(request, usuario_id):
    context = {'barra': 'nav2'}
    if request.user.is_authenticated and request.user.id == usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        if request.method == 'POST':
            modu_form = ModificaUsuario(request.POST, instance=usuario)
            if modu_form.is_valid():
                modu_form.save()
                messages.success(request,'Se ha editado la info del usuario correctamente') 
                return render(request,"appRP/publica/edita_usuario.html", {'context':context, 'modu_form':modu_form})
            else:
                messages.warning(request,'Por favor revisa los errores')
                return render(request,"appRP/publica/edita_usuario.html", {'context':context, 'modu_form':modu_form})
        else:
            modu_form = ModificaUsuario(instance=usuario)
            context = {'barra': 'nav'}
    else:
        modu_form = ModificaUsuario()
        messages.error(request,'Por favor revise los errores')
        context = {'barra': 'nav'}
    return render(request,"appRP/publica/edita_usuario.html", {'context':context, 'modu_form':modu_form})

@login_required(login_url=settings.LOGIN_URL)
def alta_producto(request):
    if request.user.is_authenticated and request.user.is_admin:
        context = {'barra': 'nav2'}
        if request.method == 'POST':
            alta_form = AltaProducto(request.POST, request.FILES)
            if alta_form.is_valid():
                alta_form.save()
                #guardar los datos en la base
                return redirect('appRP:productos')
            else:
                messages.warning(request,'Por favor revisa los errores')
        else:
            alta_form = AltaProducto()
        return render(request,'appRP/publica/alta_producto.html', {'context':context, 'alta_form':alta_form})
    return redirect('appRP:404')

@login_required(login_url=settings.LOGIN_URL)
def productos(request):
    if request.user.is_authenticated and request.user.is_admin:
        productos = Producto.objects.order_by('id')
        context = {'barra': 'nav2'}
        return render(request,'appRP/publica/lista_productos.html', {'context':context, 'productos':productos})
    else:
        return redirect('appRP:404')

@login_required(login_url=settings.LOGIN_URL)
def edita_producto(request, producto_id):
    context = {'barra': 'nav2'}
    if request.user.is_authenticated and request.user.is_admin:
        producto = Producto.objects.get(id=producto_id)
        if request.method == 'POST':
            modp_form = AltaProducto(request.POST, request.FILES, instance=producto)
            if modp_form.is_valid():
                modp_form.save()
                messages.success(request,'Se ha editado la info del producto correctamente') 
                return render(request,"appRP/publica/edita_producto.html", {'context':context, 'modp_form':modp_form})
            else:
                messages.warning(request,'Por favor revisa los errores')
                return render(request,"appRP/publica/edita_producto.html", {'context':context, 'modp_form':modp_form})
        else:
            modp_form = AltaProducto(instance=producto)
            context = {'barra': 'nav'}
            return render(request,"appRP/publica/edita_producto.html", {'context':context, 'modp_form':modp_form})
    else:
        return redirect('appRP:404')

@login_required(login_url=settings.LOGIN_URL)
def elimina_producto(request, producto_id):
    if request.user.is_authenticated and request.user.is_admin:
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        return redirect('appRP:productos')
    else:
        return redirect('appRP:404')

def error(request):
    context = {'barra': 'nav2'}
    return render(request,'appRP/publica/404.html', context)