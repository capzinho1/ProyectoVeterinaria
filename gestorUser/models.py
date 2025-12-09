from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class CitaMedica(models.Model):
    TIPO_MASCOTA_CHOICES = [
        ('gato', 'Gato'),
        ('perro', 'Perro'),
        ('ave', 'Ave'),
        ('conejo', 'Conejo'),
        ('hamster', 'Hamster'),
        ('otro', 'Otro'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="citas")
    mascota = models.CharField(max_length=100, verbose_name='Nombre de Mascota')
    tipo_mascota = models.CharField(max_length=10, choices=TIPO_MASCOTA_CHOICES, default='otro', verbose_name='Tipo de Mascota')
    titular = models.CharField(max_length=100, blank=True, null=True)  # Owner's name
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(blank=True, null=True)

    class Meta:
        pass

    def clean(self):
        """Validación del modelo para citas médicas."""
        from datetime import datetime
        
        # Validar que fecha y hora estén presentes
        if not self.fecha or not self.hora:
            return  # Dejar que el formulario valide los campos requeridos
        
        # Check if appointment datetime is in the past
        try:
            # Combinar fecha y hora en un datetime naive
            cita_datetime_naive = datetime.combine(self.fecha, self.hora)
            # Convertir a datetime con timezone
            cita_datetime = timezone.make_aware(cita_datetime_naive)
            
            # Comparar con el momento actual
            if cita_datetime < timezone.now():
                raise ValidationError("No se puede agendar una cita en el pasado.")
        except (ValueError, TypeError) as e:
            # Si hay error al combinar fecha/hora, dejar que el formulario lo maneje
            pass

        # Check for overlapping appointments globally
        overlapping = CitaMedica.objects.filter(fecha=self.fecha, hora=self.hora).exclude(pk=self.pk if self.pk else None)
        if overlapping.exists():
            raise ValidationError("Ya hay una cita agendada para esa fecha y hora.")

    def __str__(self):
        return f"Cita de {self.mascota} con {self.user.username} el {self.fecha} a las {self.hora}"
from django.contrib.auth.models import User

class VeterinarioProfile(models.Model):
    """
    Perfil extendido para usuarios veterinarios.
    
    Este modelo almacena información profesional y de configuración específica
    para usuarios que son veterinarios. Se relaciona con el modelo User de Django
    mediante una relación OneToOne (un usuario = un perfil).
    
    Campos agregados en la expansión del sistema:
    - Datos profesionales: registro, teléfono, dirección, especialidades
    - Horarios de atención: configuración por día de la semana
    
    IMPORTANTE: El campo 'es_veterinario' debe estar en True para que el usuario
    tenga acceso al sistema de veterinario. Se verifica en las vistas mediante
    la función helper es_veterinario(user).
    """
    # Relación OneToOne: cada usuario puede tener solo un perfil de veterinario
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Flag principal que indica si el usuario es veterinario activo
    # Si está en False, el usuario no tendrá acceso al sistema de veterinario
    es_veterinario = models.BooleanField(default=False, 
                                        verbose_name='Es Veterinario',
                                        help_text='Marque si este usuario es veterinario')
    
    # ========== DATOS PROFESIONALES ==========
    # Registro profesional del veterinario (número de colegiatura, etc.)
    registro_profesional = models.CharField(max_length=50, blank=True, null=True, 
                                           verbose_name='Registro Profesional',
                                           help_text='Número de registro profesional')
    
    # Teléfono de contacto del veterinario
    telefono = models.CharField(max_length=20, blank=True, null=True, 
                               verbose_name='Teléfono',
                               help_text='Teléfono de contacto')
    
    # Dirección del consultorio o lugar de trabajo
    direccion = models.TextField(blank=True, null=True, 
                                verbose_name='Dirección',
                                help_text='Dirección del consultorio')
    
    # Especialidades médicas del veterinario (separadas por comas)
    # Ejemplo: "Cirugía, Dermatología, Cardiología"
    especialidades = models.CharField(max_length=500, blank=True, null=True, 
                                     verbose_name='Especialidades (separadas por comas)',
                                     help_text='Especialidades médicas, separadas por comas')
    
    # ========== HORARIOS DE ATENCIÓN ==========
    # Configuración de horarios por día de la semana
    # Formato sugerido: "09:00 - 18:00" o "Cerrado"
    horario_lunes = models.CharField(max_length=100, blank=True, null=True, 
                                    default='09:00 - 18:00',
                                    verbose_name='Horario Lunes')
    horario_martes = models.CharField(max_length=100, blank=True, null=True, 
                                     default='09:00 - 18:00',
                                     verbose_name='Horario Martes')
    horario_miercoles = models.CharField(max_length=100, blank=True, null=True, 
                                        default='09:00 - 18:00',
                                        verbose_name='Horario Miércoles')
    horario_jueves = models.CharField(max_length=100, blank=True, null=True, 
                                     default='09:00 - 18:00',
                                     verbose_name='Horario Jueves')
    horario_viernes = models.CharField(max_length=100, blank=True, null=True, 
                                      default='09:00 - 18:00',
                                      verbose_name='Horario Viernes')
    horario_sabado = models.CharField(max_length=100, blank=True, null=True, 
                                     default='09:00 - 13:00',
                                     verbose_name='Horario Sábado')
    horario_domingo = models.CharField(max_length=100, blank=True, null=True, 
                                      default='Cerrado',
                                      verbose_name='Horario Domingo')

    def __str__(self):
        return f"Veterinario profile for {self.user.username} - Veterinario: {self.es_veterinario}"


# ==================== MODELOS DEL SISTEMA DE VETERINARIO ====================
#
# Los siguientes modelos fueron creados para el sistema completo de gestión veterinaria.
# Permiten gestionar pacientes, consultas, recetas, vacunas, tratamientos e inventario médico.
# Todos los modelos están relacionados entre sí mediante ForeignKeys para mantener
# la integridad referencial y permitir consultas eficientes.
#

class Mascota(models.Model):
    """
    Modelo para representar a los pacientes (mascotas).
    
    Este es el modelo central del sistema veterinario. Cada mascota pertenece a un
    propietario (User) y puede tener múltiples fichas clínicas, consultas, vacunas
    y tratamientos asociados.
    
    El campo 'activa' permite hacer soft delete (eliminación lógica) sin perder
    el historial médico de la mascota.
    
    Relaciones:
    - ForeignKey a User (propietario): Cada mascota tiene un dueño
    - Relación inversa con FichaClinica, Consulta, Vacuna, Tratamiento
    """
    TIPO_MASCOTA_CHOICES = [
        ('gato', 'Gato'),
        ('perro', 'Perro'),
        ('ave', 'Ave'),
        ('conejo', 'Conejo'),
        ('hamster', 'Hamster'),
        ('otro', 'Otro'),
    ]
    
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    # Relación con el propietario (cliente dueño de la mascota)
    # CASCADE: Si se elimina el usuario, se eliminan sus mascotas
    # related_name='mascotas': Permite acceder a las mascotas desde user.mascotas
    propietario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='mascotas', 
        verbose_name='Propietario'
    )
    
    # Nombre de la mascota (obligatorio)
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Mascota')
    
    # Tipo de animal (Perro, Gato, etc.) - Campo con opciones predefinidas
    tipo_mascota = models.CharField(
        max_length=10, 
        choices=TIPO_MASCOTA_CHOICES, 
        verbose_name='Tipo de Mascota'
    )
    
    # Raza del animal (opcional)
    raza = models.CharField(max_length=100, blank=True, null=True, verbose_name='Raza')
    
    # Sexo: Macho o Hembra (opcional)
    sexo = models.CharField(
        max_length=10, 
        choices=SEXO_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name='Sexo'
    )
    
    # Edad de la mascota (opcional)
    edad = models.CharField(max_length=50, blank=True, null=True, verbose_name='Edad', help_text='Ej: 2 años, 6 meses, etc.')
    
    # Color del pelaje (opcional)
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Color')
    
    # Peso en kilogramos (opcional, permite decimales)
    # max_digits=6: máximo 6 dígitos totales, decimal_places=2: 2 decimales
    peso = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name='Peso (kg)'
    )
    
    # Observaciones generales sobre la mascota (opcional)
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    # Fecha de registro automática (se establece al crear el registro)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Campo para soft delete: si está en False, la mascota está "eliminada" pero se conserva el historial
    # Permite ocultar mascotas sin perder información médica
    activa = models.BooleanField(default=True, verbose_name='Activa')
    
    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_mascota_display()} de {self.propietario.username}"


class FichaClinica(models.Model):
    """
    Modelo para fichas clínicas de las mascotas.
    
    La ficha clínica contiene el historial médico completo del paciente,
    incluyendo alergias, medicamentos permanentes y notas generales.
    Se actualiza cada vez que se modifica, manteniendo un historial completo.
    """
    # Mascota a la que pertenece esta ficha clínica (obligatorio)
    # CASCADE: Si se elimina la mascota, se elimina su ficha clínica
    mascota = models.ForeignKey(
        Mascota, 
        on_delete=models.CASCADE, 
        related_name='fichas_clinicas', 
        verbose_name='Mascota'
    )
    
    # Veterinario responsable de esta ficha clínica
    # SET_NULL: Si se elimina el veterinario, la ficha se mantiene pero sin veterinario
    veterinario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='fichas_clinicas', 
        verbose_name='Veterinario'
    )
    
    # Fecha de creación automática (se establece solo al crear)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Fecha de Creación'
    )
    
    # Fecha de última actualización automática (se actualiza cada vez que se guarda)
    fecha_actualizacion = models.DateTimeField(
        auto_now=True, 
        verbose_name='Última Actualización'
    )
    
    # Historial médico completo de la mascota (opcional)
    historial_medico = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Historial Médico'
    )
    
    # Alergias conocidas de la mascota (opcional, importante para evitar reacciones)
    alergias = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Alergias Conocidas'
    )
    
    # Medicamentos que la mascota toma de forma permanente (opcional)
    medicamentos_permanentes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Medicamentos Permanentes'
    )
    
    # Notas generales adicionales sobre la mascota (opcional)
    notas_generales = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Notas Generales'
    )
    
    class Meta:
        verbose_name = 'Ficha Clínica'
        verbose_name_plural = 'Fichas Clínicas'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"Ficha de {self.mascota.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y')}"


class Consulta(models.Model):
    """
    Modelo para representar consultas médicas realizadas a las mascotas.
    
    Una consulta puede estar relacionada con una cita médica (opcional) y contiene
    toda la información de la atención: diagnóstico, síntomas, tratamiento, etc.
    También incluye información de facturación (costo, pagada).
    """
    # Opciones de estado de la consulta
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),      # Consulta agendada pero no atendida
        ('en_proceso', 'En Proceso'),    # Consulta en curso
        ('completada', 'Completada'),    # Consulta finalizada
        ('cancelada', 'Cancelada'),      # Consulta cancelada
    ]
    
    # Relación opcional con la cita médica que originó esta consulta
    # SET_NULL: Si se elimina la cita, la consulta se mantiene pero sin cita relacionada
    cita = models.ForeignKey(
        CitaMedica, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='consultas', 
        verbose_name='Cita Relacionada'
    )
    
    # Mascota atendida en esta consulta (obligatorio)
    # CASCADE: Si se elimina la mascota, se eliminan sus consultas
    mascota = models.ForeignKey(
        Mascota, 
        on_delete=models.CASCADE, 
        related_name='consultas', 
        verbose_name='Mascota'
    )
    
    # Veterinario que realiza la consulta
    # SET_NULL: Si se elimina el veterinario, la consulta se mantiene pero sin veterinario
    veterinario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='consultas_realizadas', 
        verbose_name='Veterinario'
    )
    
    # Fecha y hora de la consulta (por defecto: ahora)
    fecha_consulta = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Consulta')
    
    # Motivo de la consulta (obligatorio)
    motivo = models.TextField(verbose_name='Motivo de Consulta')
    
    # Síntomas observados (opcional)
    sintomas = models.TextField(blank=True, null=True, verbose_name='Síntomas')
    
    # Diagnóstico realizado por el veterinario (opcional, se completa durante la consulta)
    diagnostico = models.TextField(blank=True, null=True, verbose_name='Diagnóstico')
    
    # Tratamiento prescrito (opcional)
    tratamiento = models.TextField(blank=True, null=True, verbose_name='Tratamiento')
    
    # Observaciones adicionales (opcional)
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    # Estado actual de la consulta (por defecto: pendiente)
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente', 
        verbose_name='Estado'
    )
    
    # Costo de la consulta (por defecto: 0)
    costo = models.DecimalField(
        max_digits=10,      # Máximo 10 dígitos
        decimal_places=2,   # 2 decimales (para centavos)
        default=0, 
        verbose_name='Costo de Consulta'
    )
    
    # Indicador de si la consulta ya fue pagada (por defecto: False)
    pagada = models.BooleanField(default=False, verbose_name='Pagada')
    
    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-fecha_consulta']
    
    def __str__(self):
        return f"Consulta de {self.mascota.nombre} - {self.fecha_consulta.strftime('%d/%m/%Y %H:%M')}"


class Receta(models.Model):
    """Recetas médicas"""
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='recetas', verbose_name='Consulta')
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Emisión')
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recetas_emitidas', verbose_name='Veterinario')
    instrucciones = models.TextField(verbose_name='Instrucciones')
    valida_hasta = models.DateField(blank=True, null=True, verbose_name='Válida Hasta')
    
    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Receta para {self.consulta.mascota.nombre} - {self.fecha_emision.strftime('%d/%m/%Y')}"


class Prescripcion(models.Model):
    """Prescripciones de medicamentos en recetas"""
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='prescripciones', verbose_name='Receta')
    medicamento = models.CharField(max_length=200, verbose_name='Medicamento')
    dosis = models.CharField(max_length=200, verbose_name='Dosis')
    frecuencia = models.CharField(max_length=200, verbose_name='Frecuencia')
    duracion = models.CharField(max_length=200, verbose_name='Duración')
    cantidad = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    notas = models.TextField(blank=True, null=True, verbose_name='Notas Adicionales')
    
    class Meta:
        verbose_name = 'Prescripción'
        verbose_name_plural = 'Prescripciones'
    
    def __str__(self):
        return f"{self.medicamento} - {self.dosis}"


class Vacuna(models.Model):
    """Historial de vacunas"""
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='vacunas', verbose_name='Mascota')
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vacunas_aplicadas', verbose_name='Veterinario')
    nombre_vacuna = models.CharField(max_length=200, verbose_name='Nombre de la Vacuna')
    fecha_aplicacion = models.DateField(verbose_name='Fecha de Aplicación')
    fecha_proxima = models.DateField(blank=True, null=True, verbose_name='Próxima Aplicación')
    lote = models.CharField(max_length=100, blank=True, null=True, verbose_name='Número de Lote')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    class Meta:
        verbose_name = 'Vacuna'
        verbose_name_plural = 'Vacunas'
        ordering = ['-fecha_aplicacion']
    
    def __str__(self):
        return f"{self.nombre_vacuna} - {self.mascota.nombre} ({self.fecha_aplicacion.strftime('%d/%m/%Y')})"


class Tratamiento(models.Model):
    """Historial de tratamientos"""
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='tratamientos', verbose_name='Mascota')
    consulta = models.ForeignKey(Consulta, on_delete=models.SET_NULL, null=True, blank=True, related_name='tratamientos', verbose_name='Consulta Relacionada')
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tratamientos_asignados', verbose_name='Veterinario')
    nombre_tratamiento = models.CharField(max_length=200, verbose_name='Nombre del Tratamiento')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Fin')
    descripcion = models.TextField(verbose_name='Descripcion del Tratamiento')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name='Estado')
    notas = models.TextField(blank=True, null=True, verbose_name='Notas')
    
    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre_tratamiento} - {self.mascota.nombre}"


class EgresoMedicamento(models.Model):
    """Registro de egresos de medicamentos del inventario"""
    consulta = models.ForeignKey(Consulta, on_delete=models.SET_NULL, null=True, blank=True, related_name='egresos_medicamentos', verbose_name='Consulta Relacionada')
    medicamento = models.CharField(max_length=200, verbose_name='Medicamento')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad Egresada')
    fecha_egreso = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Egreso')
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='egresos_realizados', verbose_name='Veterinario Responsable')
    motivo = models.TextField(verbose_name='Motivo del Egreso')
    paciente = models.CharField(max_length=200, blank=True, null=True, verbose_name='Paciente')
    
    class Meta:
        verbose_name = 'Egreso de Medicamento'
        verbose_name_plural = 'Egresos de Medicamentos'
        ordering = ['-fecha_egreso']
    
    def __str__(self):
        return f"Egreso: {self.medicamento} - Cantidad: {self.cantidad} - {self.fecha_egreso.strftime('%d/%m/%Y')}"
