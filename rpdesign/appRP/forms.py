from django import forms
from .models import Usuario, Producto, Orden

from django.contrib.auth.forms import UserCreationForm

FORMATOS = [(0, 'Seleccione un formato'),
            ('15 cm x 20 cm', '15 cm x 20 cm'),
            ('20 cm x 25 cm', '20 cm x 25 cm'),
            ('30 cm x 40 cm', '30 cm x 40 cm')]

class AltaProducto(forms.ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':"form-control", 'id':"name", 'placeholder':"nombre", 'required':True}),
            'descripcion' : forms.TextInput(attrs={'class':"form-control", 'id':"description", 'placeholder':"descripción", 'required':True}),
            'formato' : forms.Select(attrs={'class':"form-select", 'id':"format"}, choices=FORMATOS),
            'precio' : forms.NumberInput(attrs={'class':"form-control", 'id':"price", 'placeholder':"100", 'required':True}),
            'imagen' : forms.FileInput(attrs={'class':"form-control", 'id':"linkPhoto",}),
                }


class AltaUsuario(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'dni', 'username', 'calle', 'altura', 'piso', 
            'depto', 'localidad', 'cod_postal', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Añadir atributos personalizados a un campo.
        self.fields['first_name'].widget.attrs.update({'placeholder': 'nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'apellido'})

    def clean_username(self):
        username = self.cleaned_data['username']
        username_taken = Usuario.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('El nombre de usuario ya esta en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        email_taken = Usuario.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('El email ya esta en uso.')
        return email

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        dni_taken = Usuario.objects.filter(dni=dni).exists()
        if dni_taken:
            raise forms.ValidationError('El dni ya esta en uso.')
        return dni


class ModificaUsuario(forms.ModelForm):
    
    class Meta:
        model = Usuario
        # Los campos a modificar, excepto "password".
        fields = ['first_name', 'last_name', 'email', 'dni', 'username', 
                'calle', 'altura', 'piso', 'depto', 'localidad', 'cod_postal']
        

# FORMULARIOS PARA EL CARRITO

CANTIDAD_PRODUCTO = [(i, str(i)) for i in range(1, 21)]

class CarritoAgregaProducto(forms.Form):
    cantidad = forms.TypedChoiceField(
                                choices=CANTIDAD_PRODUCTO,
                                coerce=int)
    anular = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
    

# FORMULARIO PARA LAS ORDENES

class CrearOrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['first_name', 'last_name', 'email', 'calle', 'altura', 'piso',
                     'depto', 'localidad', 'cod_postal']
        labels = {'first_name': 'Nombre', 'last_name': 'Apellido', }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})