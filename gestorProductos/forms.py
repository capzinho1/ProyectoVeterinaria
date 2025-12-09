from django import forms
from .models import (
    Productos, PCProductos, PAProductos, PSProductos, AProductos,
    Categoria, AGAProductos, AGCProductos, SnackGProductos, SnackPProductos,
    Antiparasitario, Medicamento, Shampoo, Cama, Collar, Juguete
)
from gestorUser.models import CitaMedica

# -------------------------------
# FORMULARIOS PRODUCTOS GENERALES
# -------------------------------
class ProductosRegistroForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Reutilización del widget base
BASE_WIDGETS = ProductosRegistroForm.Meta.widgets

class PCProductosForm(forms.ModelForm):
    class Meta:
        model = PCProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class PAProductosForm(forms.ModelForm):
    class Meta:
        model = PAProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class PSProductosForm(forms.ModelForm):
    class Meta:
        model = PSProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class AProductosForm(forms.ModelForm):
    class Meta:
        model = AProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

# -------------------------------
# FORMULARIO CATEGORIAS
# -------------------------------
class CategoriaRegistroForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'mascota': forms.TextInput(attrs={'class': 'form-control'}),
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cuidado': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_alimento': forms.TextInput(attrs={'class': 'form-control'}),
            'accesorios': forms.TextInput(attrs={'class': 'form-control'}),
            'medicamentos': forms.TextInput(attrs={'class': 'form-control'}),
            'servicios_asociados': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -------------------------------
# FORMULARIOS ALIMENTOS GATO
# -------------------------------
class AGAProductosForm(forms.ModelForm):
    class Meta:
        model = AGAProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class AGCProductosForm(forms.ModelForm):
    class Meta:
        model = AGCProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

# -------------------------------
# FORMULARIOS SNACKS
# -------------------------------
class SnackGProductosForm(forms.ModelForm):
    class Meta:
        model = SnackGProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class SnackPProductosForm(forms.ModelForm):
    class Meta:
        model = SnackPProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

# -------------------------------
# FORMULARIOS MEDICAMENTOS
# -------------------------------
class AntiparasitarioForm(forms.ModelForm):
    class Meta:
        model = Antiparasitario
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

# -------------------------------
# FORMULARIO SHAMPOOS
# -------------------------------
class ShampooForm(forms.ModelForm):
    class Meta:
        model = Shampoo
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -------------------------------
# FORMULARIO CAMAS
# -------------------------------
class CamaForm(forms.ModelForm):
    class Meta:
        model = Cama
        fields = '__all__'
        widgets = {
            **BASE_WIDGETS,
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -------------------------------
# FORMULARIO COLLARES
# -------------------------------
class CollarForm(forms.ModelForm):
    class Meta:
        model = Collar
        fields = '__all__'
        widgets = {
            **BASE_WIDGETS,
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -------------------------------
# FORMULARIO JUGUETES
# -------------------------------
class JugueteForm(forms.ModelForm):
    class Meta:
        model = Juguete
        fields = '__all__'
        widgets = {
            **BASE_WIDGETS,
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
        }

#---------------------------------------------------
#CREAR CITA
#---------------------------------------------------
class CitaVeterinariaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = '__all__'
        widgets = {
            'nombre_mascota': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_mascota': forms.Select(attrs={'class': 'form-select'}),
            'nombre_titular': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_cita': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ----------------------------------------------------
# FORMULARIOS ESPECIALES PARA DATATABLES (EDICIÓN)
# ----------------------------------------------------
class DatatableProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableProductosPCForm(forms.ModelForm):
    class Meta:
        model = PCProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableProductosPAForm(forms.ModelForm):
    class Meta:
        model = PAProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableProductosPSForm(forms.ModelForm):
    class Meta:
        model = PSProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableProductosAForm(forms.ModelForm):
    class Meta:
        model = AProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

# -------------------------------
# FORMULARIOS ESPECIALES PARA DATATABLES (EDICIÓN) - ADICIONALES
# -------------------------------
class DatatableAGAForm(forms.ModelForm):
    class Meta:
        model = AGAProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableAGCForm(forms.ModelForm):
    class Meta:
        model = AGCProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableSnackGForm(forms.ModelForm):
    class Meta:
        model = SnackGProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableSnackPForm(forms.ModelForm):
    class Meta:
        model = SnackPProductos
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableAntiparasitarioForm(forms.ModelForm):
    class Meta:
        model = Antiparasitario
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class DatatableMedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class DatatableShampooForm(forms.ModelForm):
    class Meta:
        model = Shampoo
        fields = '__all__'
        widgets = BASE_WIDGETS

class DatatableCollarForm(forms.ModelForm):
    class Meta:
        model = Collar
        fields = '__all__'
        widgets = {
            **BASE_WIDGETS,
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DatatableCamaForm(forms.ModelForm):
    class Meta:
        model = Cama
        fields = '__all__'
        widgets = {
            **BASE_WIDGETS,
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DatatableJugueteForm(forms.ModelForm):
    class Meta:
        model = Juguete
        fields = '__all__'
        widgets = {
            **BASE_WIDGETS,
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -------------------------------
# FORMULARIO DE CHECKOUT
# -------------------------------
class CheckoutForm(forms.Form):
    """Formulario para completar el proceso de compra antes de la pasarela de pago"""
    
    # Datos del cliente
    nombre_completo = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo'
        }),
        label='Nombre Completo'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        }),
        label='Correo Electrónico'
    )
    
    telefono = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 1234 5678'
        }),
        label='Teléfono'
    )
    
    # Dirección de envío
    direccion = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calle, número, departamento'
        }),
        label='Dirección'
    )
    
    ciudad = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad'
        }),
        label='Ciudad'
    )
    
    codigo_postal = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567'
        }),
        label='Código Postal'
    )
    
    # Método de pago
    METODO_PAGO_CHOICES = [
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Pago contra entrega'),
    ]
    
    metodo_pago = forms.ChoiceField(
        choices=METODO_PAGO_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Método de Pago'
    )
    
    # Información de tarjeta (opcional, solo si método es tarjeta)
    numero_tarjeta = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'maxlength': '19'
        }),
        label='Número de Tarjeta'
    )
    
    fecha_vencimiento = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/AA',
            'maxlength': '5'
        }),
        label='Fecha de Vencimiento (MM/AA)'
    )
    
    cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'maxlength': '4',
            'type': 'password'
        }),
        label='CVV'
    )
    
    # Notas adicionales
    notas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Instrucciones adicionales para la entrega (opcional)'
        }),
        label='Notas Adicionales'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        metodo_pago = cleaned_data.get('metodo_pago')
        numero_tarjeta = cleaned_data.get('numero_tarjeta')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
        cvv = cleaned_data.get('cvv')
        
        # Si el método de pago es tarjeta, validar campos de tarjeta
        if metodo_pago == 'tarjeta':
            if not numero_tarjeta:
                raise forms.ValidationError({
                    'numero_tarjeta': 'El número de tarjeta es requerido cuando se selecciona pago con tarjeta.'
                })
            if not fecha_vencimiento:
                raise forms.ValidationError({
                    'fecha_vencimiento': 'La fecha de vencimiento es requerida cuando se selecciona pago con tarjeta.'
                })
            if not cvv:
                raise forms.ValidationError({
                    'cvv': 'El CVV es requerido cuando se selecciona pago con tarjeta.'
                })
        
        return cleaned_data
