from django import forms
from .models import (
    CitaMedica, VeterinarioProfile, Mascota, FichaClinica, Consulta,
    Receta, Prescripcion, Vacuna, Tratamiento, EgresoMedicamento
)
from django.forms.widgets import DateInput, TimeInput
from django.contrib.auth.models import User

class CitaMedicaForm(forms.ModelForm):
    """
    Formulario mejorado para agendar citas médicas.
    
    Este formulario ha sido mejorado con las siguientes características:
    
    1. Validaciones completas:
       - No permite fechas pasadas
       - Verifica horario de atención (09:00 - 18:00)
       - Previene citas duplicadas (misma fecha y hora)
       - Valida combinación fecha+hora (no permite citas en el pasado)
    
    2. Campos obligatorios claramente marcados:
       - mascota, tipo_mascota, fecha, hora son obligatorios
       - titular y motivo son opcionales
    
    3. Mejoras de UX:
       - Placeholders informativos
       - Fecha mínima establecida automáticamente (hoy)
       - Clases CSS para campos con errores (is-invalid)
       - Labels descriptivos
    
    4. Validación en tiempo real:
       - El template incluye JavaScript para validación del lado del cliente
    """
    class Meta:
        model = CitaMedica
        fields = ['mascota', 'tipo_mascota', 'titular', 'fecha', 'hora', 'motivo']
        
        # Labels descriptivos para cada campo
        labels = {
            'mascota': 'Nombre de Mascota',
            'tipo_mascota': 'Tipo de Mascota',
            'titular': 'Nombre del Titular',
            'fecha': 'Fecha de la Cita',
            'hora': 'Hora de la Cita',
            'motivo': 'Motivo de la Consulta',
        }
        
        # Widgets personalizados con estilos Bootstrap y atributos HTML5
        widgets = {
            'mascota': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de su mascota',
                'required': True  # HTML5 required
            }),
            'tipo_mascota': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'titular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del propietario (opcional)'
            }),
            'fecha': DateInput(attrs={
                'type': 'date',  # Input tipo fecha HTML5
                'class': 'form-control',
                'required': True,
                'min': None  # Se establecerá dinámicamente en __init__
            }),
            'hora': TimeInput(attrs={
                'type': 'time',  # Input tipo hora HTML5
                'class': 'form-control',
                'required': True
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa el motivo de la consulta (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Inicialización del formulario con configuraciones dinámicas.
        
        Establece:
        - Campos obligatorios vs opcionales
        - Fecha mínima (hoy) para evitar citas pasadas
        - Clases CSS para campos con errores de validación
        """
        super().__init__(*args, **kwargs)
        
        # ========== CAMPOS OBLIGATORIOS ==========
        # Marcar explícitamente qué campos son obligatorios
        self.fields['mascota'].required = True
        self.fields['tipo_mascota'].required = True
        self.fields['fecha'].required = True
        self.fields['hora'].required = True
        
        # Campos opcionales
        self.fields['titular'].required = False
        self.fields['motivo'].required = False
        
        # ========== FECHA MÍNIMA ==========
        # Establecer la fecha mínima como hoy para evitar seleccionar fechas pasadas
        from django.utils import timezone
        fecha_minima = timezone.now().date()
        self.fields['fecha'].widget.attrs['min'] = fecha_minima.strftime('%Y-%m-%d')
        
        # ========== ESTILOS PARA ERRORES ==========
        # Si el formulario tiene errores, agregar clase 'is-invalid' de Bootstrap
        # para mostrar campos con errores visualmente (borde rojo)
        if self.errors:
            for field_name in self.errors:
                if field_name in self.fields:
                    current_class = self.fields[field_name].widget.attrs.get('class', '')
                    if 'is-invalid' not in current_class:
                        self.fields[field_name].widget.attrs['class'] = current_class + ' is-invalid'
    
    def clean_fecha(self):
        """
        Validación específica del campo 'fecha'.
        
        Verifica que la fecha no sea en el pasado.
        Se ejecuta automáticamente antes de clean().
        
        Retorna:
            date: La fecha validada
            
        Lanza:
            ValidationError: Si la fecha es en el pasado
        """
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            from django.utils import timezone
            # Comparar solo la fecha (sin hora) con la fecha actual
            if fecha < timezone.now().date():
                raise forms.ValidationError("No se puede agendar una cita en el pasado.")
        return fecha
    
    def clean(self):
        """
        Validación cruzada de campos (validación completa del formulario).
        
        Realiza validaciones que involucran múltiples campos:
        1. Verifica que fecha+hora no sea en el pasado
        2. Verifica horario de atención (09:00 - 18:00)
        3. Previene citas duplicadas (misma fecha y hora)
        
        Este método se ejecuta después de clean_<campo>() individuales.
        
        Retorna:
            dict: cleaned_data con todos los datos validados
            
        Lanza:
            ValidationError: Si hay errores de validación
        """
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        # Solo validar si ambos campos están presentes
        if fecha and hora:
            from django.utils import timezone
            from datetime import datetime
            
            # ========== VALIDACIÓN: NO CITAS EN EL PASADO ==========
            # Combinar fecha y hora, convertir a datetime con timezone
            cita_datetime = timezone.make_aware(
                datetime.combine(fecha, hora)
            )
            # Comparar con el momento actual
            if cita_datetime < timezone.now():
                raise forms.ValidationError("No se puede agendar una cita en el pasado.")
            
            # ========== VALIDACIÓN: HORARIO DE ATENCIÓN ==========
            # Definir horario de atención permitido
            hora_min = datetime.strptime('09:00', '%H:%M').time()
            hora_max = datetime.strptime('18:00', '%H:%M').time()
            
            # Verificar que la hora esté dentro del horario permitido
            if hora < hora_min:
                self.add_error('hora', "Las citas solo pueden agendarse a partir de las 09:00 horas.")
            if hora > hora_max:
                self.add_error('hora', "Las citas solo pueden agendarse hasta las 18:00 horas.")
            
            # ========== VALIDACIÓN: PREVENIR CITAS DUPLICADAS ==========
            # Verificar si ya existe una cita en esa fecha y hora
            from .models import CitaMedica
            # Obtener el PK de la instancia actual (si estamos editando)
            instance_pk = self.instance.pk if self.instance else None
            # Buscar citas con la misma fecha y hora, excluyendo la actual
            existing_cita = CitaMedica.objects.filter(
                fecha=fecha, 
                hora=hora
            ).exclude(pk=instance_pk).first()
            
            if existing_cita:
                # Agregar error a ambos campos para mejor UX
                self.add_error('fecha', "Ya existe una cita agendada para esta fecha y hora.")
                self.add_error('hora', "Por favor seleccione otra hora disponible.")
        
        return cleaned_data

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    es_veterinario = forms.BooleanField(required=False, label='Registrarse como veterinario')
    is_staff = forms.BooleanField(required=False, label='Registrar como admin (staff)')
    is_superuser = forms.BooleanField(required=False, label='Registrar como superusuario')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'es_veterinario', 'is_staff', 'is_superuser')

class CustomUserChangeForm(UserChangeForm):
    es_veterinario = forms.BooleanField(required=False, label='Es veterinario')
    is_staff = forms.BooleanField(required=False, label='Es admin (staff)')
    is_superuser = forms.BooleanField(required=False, label='Es superusuario')

    class Meta:
        model = User
        fields = ('username', 'email', 'es_veterinario', 'is_staff', 'is_superuser', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value for es_veterinario from related VeterinarioProfile
        if self.instance and hasattr(self.instance, 'veterinarioprofile'):
            self.fields['es_veterinario'].initial = self.instance.veterinarioprofile.es_veterinario
        else:
            self.fields['es_veterinario'].initial = False

    def save(self, commit=True):
        user = super().save(commit=False)
        es_veterinario = self.cleaned_data.get('es_veterinario', False)
        user.is_staff = self.cleaned_data.get('is_staff', False)
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        if commit:
            user.save()
            # Update or create VeterinarioProfile accordingly
            if es_veterinario:
                VeterinarioProfile.objects.update_or_create(user=user, defaults={'es_veterinario': True})
            else:
                # If profile exists and es_veterinario=False, delete the profile
                try:
                    profile = user.veterinarioprofile
                    profile.delete()
                except VeterinarioProfile.DoesNotExist:
                    pass
        return user

class VeterinarioProfileForm(forms.ModelForm):
    class Meta:
        model = VeterinarioProfile
        fields = (
            'registro_profesional', 'telefono', 'direccion', 'especialidades',
            'horario_lunes', 'horario_martes', 'horario_miercoles', 'horario_jueves',
            'horario_viernes', 'horario_sabado', 'horario_domingo'
        )
        widgets = {
            'registro_profesional': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'especialidades': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cirugía, Dermatología, Cardiología'}),
            'horario_lunes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 09:00 - 18:00'}),
            'horario_martes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 09:00 - 18:00'}),
            'horario_miercoles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 09:00 - 18:00'}),
            'horario_jueves': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 09:00 - 18:00'}),
            'horario_viernes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 09:00 - 18:00'}),
            'horario_sabado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 09:00 - 13:00'}),
            'horario_domingo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cerrado'}),
        }


# ==================== FORMULARIOS DEL SISTEMA DE VETERINARIO ====================

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = [
            'propietario', 'nombre', 'tipo_mascota', 'raza', 'sexo', 'fecha_nacimiento',
            'color', 'peso', 'observaciones', 'activa'
        ]
        widgets = {
            'propietario': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_mascota': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios que no sean veterinarios ni admin
        from django.contrib.auth.models import User
        self.fields['propietario'].queryset = User.objects.filter(is_staff=False, is_superuser=False)


class FichaClinicaForm(forms.ModelForm):
    class Meta:
        model = FichaClinica
        fields = [
            'historial_medico', 'alergias', 'medicamentos_permanentes', 'notas_generales'
        ]
        widgets = {
            'historial_medico': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'medicamentos_permanentes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notas_generales': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'mascota', 'motivo', 'sintomas', 'diagnostico', 'tratamiento', 'observaciones',
            'estado', 'costo', 'pagada', 'fecha_consulta'
        ]
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pagada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_consulta': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo mascotas activas
        if 'mascota' in self.fields:
            self.fields['mascota'].queryset = Mascota.objects.filter(activa=True)


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['instrucciones', 'valida_hasta']
        widgets = {
            'instrucciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'valida_hasta': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class PrescripcionForm(forms.ModelForm):
    class Meta:
        model = Prescripcion
        fields = ['medicamento', 'dosis', 'frecuencia', 'duracion', 'cantidad', 'notas']
        widgets = {
            'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre_vacuna', 'fecha_aplicacion', 'fecha_proxima', 'lote', 'observaciones']
        widgets = {
            'nombre_vacuna': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_aplicacion': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_proxima': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['nombre_tratamiento', 'fecha_inicio', 'fecha_fin', 'descripcion', 'estado', 'notas']
        widgets = {
            'nombre_tratamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EgresoMedicamentoForm(forms.ModelForm):
    class Meta:
        model = EgresoMedicamento
        fields = ['medicamento', 'cantidad', 'motivo', 'paciente']
        widgets = {
            'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'paciente': forms.TextInput(attrs={'class': 'form-control'}),
        }
