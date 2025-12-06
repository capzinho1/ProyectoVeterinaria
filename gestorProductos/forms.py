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
