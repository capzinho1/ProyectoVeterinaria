"""
Vistas del Sistema Completo de Veterinario
==========================================

Este archivo contiene todas las vistas necesarias para el módulo de veterinario.
Fue creado para separar la lógica del sistema veterinario del resto de la aplicación,
manteniendo el código organizado y fácil de mantener.

Estructura:
- Funciones Helper: Utilidades para verificar permisos
- Perfil y Configuración: Gestión del perfil del veterinario
- Gestión de Pacientes: CRUD de mascotas/pacientes
- Fichas Clínicas: Historial médico de pacientes
- Agenda y Citas: Gestión de citas médicas
- Consultas Médicas: Registro y seguimiento de consultas
- Recetas y Prescripciones: Emisión de recetas médicas
- Vacunas: Registro de vacunación
- Tratamientos: Seguimiento de tratamientos
- Inventario Médico: Control de medicamentos y alertas

Todas las vistas requieren autenticación (@login_required) y verificación
de que el usuario sea veterinario mediante la función helper.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Sum
from django.http import JsonResponse
from .models import (
    VeterinarioProfile, Mascota, FichaClinica, Consulta,
    Receta, Prescripcion, Vacuna, Tratamiento, EgresoMedicamento, CitaMedica
)
from .forms import (
    VeterinarioProfileForm, MascotaForm, FichaClinicaForm,
    ConsultaForm, RecetaForm, PrescripcionForm, VacunaForm, TratamientoForm,
    EgresoMedicamentoForm
)
from gestorProductos.models import (
    Medicamento, Antiparasitario, Productos, PCProductos, PAProductos,
    PSProductos, AProductos, AGAProductos, AGCProductos, SnackGProductos,
    SnackPProductos, Shampoo, Cama, Collar, Juguete
)


# ==================== FUNCIONES HELPER ====================

def es_veterinario(user):
    """
    Verifica si un usuario tiene perfil de veterinario activo.
    
    Parámetros:
        user: Instancia de User de Django
        
    Retorna:
        bool: True si el usuario tiene VeterinarioProfile con es_veterinario=True,
              False en caso contrario (incluye si no tiene perfil)
              
    Esta función es utilizada por todas las vistas para verificar permisos antes
    de permitir el acceso a funcionalidades del sistema veterinario.
    """
    try:
        perfil = user.veterinarioprofile  # Accede a la relación OneToOne
        return perfil.es_veterinario  # Retorna True solo si está activado
    except VeterinarioProfile.DoesNotExist:
        # Si no existe el perfil, no es veterinario
        return False


def verificar_veterinario(request):
    """
    Función helper para verificar permisos de veterinario en las vistas.
    
    Parámetros:
        request: Objeto HttpRequest de Django
        
    Retorna:
        HttpResponseRedirect o None: 
        - Si el usuario NO es veterinario, retorna un redirect con mensaje de error
        - Si el usuario ES veterinario, retorna None (continúa el flujo normal)
        
    Uso:
        check = verificar_veterinario(request)
        if check:
            return check  # Redirige si no es veterinario
        # Continúa con la lógica de la vista si pasa la verificación
    """
    if not es_veterinario(request.user):
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('vet_veterinario')  # Redirige al dashboard de veterinario
    return None  # Usuario autorizado, continúa normalmente


# ==================== PERFIL Y CONFIGURACIÓN ====================

@login_required
def vet_perfil(request):
    """
    Vista para ver y editar el perfil del veterinario.
    Permite configurar datos profesionales, horarios y especialidades.
    """
    # Verificar que el usuario es veterinario antes de continuar
    check = verificar_veterinario(request)
    if check:
        return check  # Si no es veterinario, se redirige automáticamente
    
    # Intentar obtener el perfil de veterinario del usuario actual
    try:
        # Acceder a la relación OneToOne con VeterinarioProfile
        perfil = request.user.veterinarioprofile
    except VeterinarioProfile.DoesNotExist:
        # Si no existe perfil, crearlo automáticamente y marcarlo como veterinario
        perfil = VeterinarioProfile.objects.create(
            user=request.user, 
            es_veterinario=True  # Activar automáticamente el perfil de veterinario
        )
    
    # Procesar formulario si se envió (método POST)
    if request.method == 'POST':
        # Crear formulario con los datos enviados y la instancia existente del perfil
        form = VeterinarioProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            # Guardar los cambios en la base de datos
            form.save()
            # Mostrar mensaje de éxito al usuario
            messages.success(request, "Perfil actualizado correctamente.")
            # Redirigir a la misma página para mostrar el mensaje
            return redirect('vet_perfil')
    else:
        # Si es GET, mostrar el formulario con los datos actuales del perfil
        form = VeterinarioProfileForm(instance=perfil)
    
    # Renderizar el template con el formulario y el perfil
    return render(request, 'gestorUser/veterinario/perfil.html', {
        'form': form,      # Formulario para editar (con datos actuales o vacío)
        'perfil': perfil   # Instancia del perfil para mostrar información adicional
    })


# ==================== GESTIÓN DE PACIENTES (MASCOTAS) ====================

@login_required
def vet_pacientes(request):
    """
    Vista para listar todos los pacientes (mascotas) del sistema.
    Incluye funcionalidad de búsqueda por nombre, propietario o raza.
    """
    # Verificar permisos: solo veterinarios pueden ver esta vista
    check = verificar_veterinario(request)
    if check:
        return check  # Redirige si no es veterinario
    
    # Obtener el término de búsqueda desde los parámetros GET de la URL
    # Si no hay búsqueda, search será una cadena vacía
    search = request.GET.get('search', '')
    
    # Obtener todos los pacientes activos (campo activa=True permite soft delete)
    pacientes = Mascota.objects.filter(activa=True)
    
    # Si hay un término de búsqueda, filtrar los pacientes
    if search:
        # Usar Q objects para hacer búsqueda OR en múltiples campos
        # icontains hace búsqueda case-insensitive (no diferencia mayúsculas/minúsculas)
        pacientes = pacientes.filter(
            Q(nombre__icontains=search) |                    # Buscar en nombre de mascota
            Q(propietario__username__icontains=search) |     # Buscar en username del propietario
            Q(raza__icontains=search)                        # Buscar en raza
        )
    
    # Optimizar consulta: select_related trae el propietario en la misma consulta SQL
    # Ordenar por fecha de registro descendente (más recientes primero)
    pacientes = pacientes.select_related('propietario').order_by('-fecha_registro')
    
    # Renderizar template con la lista de pacientes y el término de búsqueda
    return render(request, 'gestorUser/veterinario/pacientes_lista.html', {
        'pacientes': pacientes,  # Lista de pacientes (filtrados si hay búsqueda)
        'search': search         # Término de búsqueda para mantenerlo en el input
    })


@login_required
def vet_paciente_detalle(request, paciente_id):
    """
    Vista para ver el detalle completo de un paciente.
    Muestra información básica, ficha clínica, consultas, vacunas y tratamientos.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Obtener el paciente por su ID, devolver 404 si no existe
    paciente = get_object_or_404(Mascota, id=paciente_id)
    
    # Buscar la ficha clínica del paciente (puede no tener una)
    # first() devuelve el primer resultado o None si no encuentra
    ficha_clinica = FichaClinica.objects.filter(mascota=paciente).first()
    
    # Obtener las últimas 10 consultas del paciente, ordenadas por fecha descendente (más recientes primero)
    consultas = Consulta.objects.filter(
        mascota=paciente
    ).order_by('-fecha_consulta')[:10]  # Limitar a 10 resultados
    
    # Obtener las últimas 10 vacunas aplicadas al paciente, ordenadas por fecha
    vacunas = Vacuna.objects.filter(
        mascota=paciente
    ).order_by('-fecha_aplicacion')[:10]  # Limitar a 10 resultados
    
    # Obtener los últimos 10 tratamientos del paciente, ordenados por fecha de inicio
    tratamientos = Tratamiento.objects.filter(
        mascota=paciente
    ).order_by('-fecha_inicio')[:10]  # Limitar a 10 resultados
    
    # Renderizar template con toda la información del paciente
    return render(request, 'gestorUser/veterinario/paciente_detalle.html', {
        'paciente': paciente,          # Información básica del paciente
        'ficha_clinica': ficha_clinica, # Ficha clínica (puede ser None)
        'consultas': consultas,        # Historial de consultas (últimas 10)
        'vacunas': vacunas,            # Historial de vacunas (últimas 10)
        'tratamientos': tratamientos   # Historial de tratamientos (últimos 10)
    })


@login_required
def vet_paciente_crear(request):
    """
    Vista para crear un nuevo paciente (mascota) en el sistema.
    Permite registrar la información básica de la mascota.
    """
    # Verificar que el usuario es veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Procesar formulario si se envió (método POST)
    if request.method == 'POST':
        # Crear formulario con los datos enviados por el usuario
        form = MascotaForm(request.POST)
        if form.is_valid():
            # Guardar sin commit para poder modificar antes de guardar en BD
            mascota = form.save(commit=False)
            
            # Si el formulario no especificó un propietario, usar el usuario actual como propietario
            # Esto es útil cuando el veterinario crea un paciente desde cero
            if not mascota.propietario_id:
                mascota.propietario = request.user
            
            # Guardar el paciente en la base de datos
            mascota.save()
            
            # Mostrar mensaje de éxito con el nombre del paciente creado
            messages.success(request, f"Paciente {mascota.nombre} creado correctamente.")
            
            # Redirigir a la página de detalle del paciente recién creado
            return redirect('vet_paciente_detalle', paciente_id=mascota.id)
    else:
        # Si es GET, mostrar formulario vacío para crear nuevo paciente
        form = MascotaForm()
    
    # Renderizar template con el formulario
    return render(request, 'gestorUser/veterinario/paciente_form.html', {
        'form': form,                           # Formulario vacío para crear
        'titulo': 'Crear Nuevo Paciente'        # Título para mostrar en el template
    })


@login_required
def vet_paciente_editar(request, paciente_id):
    """Editar paciente existente"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    paciente = get_object_or_404(Mascota, id=paciente_id)
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, f"Paciente {paciente.nombre} actualizado correctamente.")
            return redirect('vet_paciente_detalle', paciente_id=paciente.id)
    else:
        form = MascotaForm(instance=paciente)
    
    return render(request, 'gestorUser/veterinario/paciente_form.html', {
        'form': form,
        'paciente': paciente,
        'titulo': f'Editar Paciente: {paciente.nombre}'
    })


# ==================== FICHAS CLÍNICAS ====================

@login_required
def vet_fichas_clinicas(request):
    """
    Vista para listar todas las fichas clínicas del sistema.
    Incluye funcionalidad de búsqueda por nombre de mascota.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Obtener todas las fichas clínicas con optimización de consultas
    # select_related trae las relaciones mascota y veterinario en la misma consulta SQL
    # Ordenar por fecha de actualización descendente (más recientes primero)
    fichas = FichaClinica.objects.select_related(
        'mascota',      # Traer datos de la mascota
        'veterinario'   # Traer datos del veterinario
    ).order_by('-fecha_actualizacion')
    
    # Obtener término de búsqueda desde los parámetros GET de la URL
    search = request.GET.get('search', '')
    
    # Si hay búsqueda, filtrar fichas por nombre de mascota
    if search:
        # mascota__nombre__icontains: busca en el nombre de la mascota relacionada
        # icontains hace búsqueda case-insensitive (no diferencia mayúsculas/minúsculas)
        fichas = fichas.filter(mascota__nombre__icontains=search)
    
    # Renderizar template con la lista de fichas
    return render(request, 'gestorUser/veterinario/fichas_lista.html', {
        'fichas': fichas,  # Lista de fichas (filtradas si hay búsqueda)
        'search': search   # Término de búsqueda para mantenerlo en el input
    })


@login_required
def vet_ficha_detalle(request, ficha_id):
    """
    Vista para ver el detalle completo de una ficha clínica.
    Muestra la ficha junto con el historial completo: consultas, vacunas y tratamientos.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Obtener la ficha clínica por su ID, devolver 404 si no existe
    ficha = get_object_or_404(FichaClinica, id=ficha_id)
    
    # Obtener todas las consultas de la mascota asociada a esta ficha
    # Ordenadas por fecha descendente (más recientes primero)
    consultas = Consulta.objects.filter(
        mascota=ficha.mascota
    ).order_by('-fecha_consulta')
    
    # Obtener todas las vacunas aplicadas a la mascota
    # Ordenadas por fecha de aplicación descendente
    vacunas = Vacuna.objects.filter(
        mascota=ficha.mascota
    ).order_by('-fecha_aplicacion')
    
    # Obtener todos los tratamientos de la mascota
    # Ordenados por fecha de inicio descendente
    tratamientos = Tratamiento.objects.filter(
        mascota=ficha.mascota
    ).order_by('-fecha_inicio')
    
    # ========== CALCULAR RESUMEN FINANCIERO ==========
    # Calcular totales de costos de las consultas
    from django.db.models import Sum
    total_consultas = consultas.count()
    costo_total = consultas.aggregate(total=Sum('costo'))['total'] or 0
    costo_pagado = consultas.filter(pagada=True).aggregate(total=Sum('costo'))['total'] or 0
    costo_pendiente = costo_total - costo_pagado
    
    # Renderizar template con toda la información de la ficha clínica
    return render(request, 'gestorUser/veterinario/ficha_detalle.html', {
        'ficha': ficha,              # Información de la ficha clínica
        'consultas': consultas,      # Historial completo de consultas
        'vacunas': vacunas,          # Historial completo de vacunas
        'tratamientos': tratamientos, # Historial completo de tratamientos
        'total_consultas': total_consultas,  # Total de consultas
        'costo_total': costo_total,           # Costo total de todas las consultas
        'costo_pagado': costo_pagado,         # Costo total pagado
        'costo_pendiente': costo_pendiente    # Costo pendiente de pago
    })


@login_required
def vet_ficha_crear(request, paciente_id):
    """
    Vista para crear una nueva ficha clínica para un paciente específico.
    Una mascota solo puede tener una ficha clínica activa.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Obtener el paciente por su ID, devolver 404 si no existe
    paciente = get_object_or_404(Mascota, id=paciente_id)
    
    # ========== VERIFICAR FICHA CLÍNICA EXISTENTE ==========
    # Buscar si este paciente ya tiene una ficha clínica creada
    ficha_existente = FichaClinica.objects.filter(mascota=paciente).first()
    
    if ficha_existente:
        # Si ya existe, informar al usuario y redirigir a editar en lugar de crear nueva
        messages.info(request, "Este paciente ya tiene una ficha clínica. Puedes editarla.")
        return redirect('vet_ficha_editar', ficha_id=ficha_existente.id)
    
    # ========== CREAR NUEVA FICHA CLÍNICA ==========
    # Procesar formulario si se envió (POST)
    if request.method == 'POST':
        # Crear formulario con los datos enviados
        form = FichaClinicaForm(request.POST)
        if form.is_valid():
            # Guardar la ficha clínica junto con múltiples vacunas y tratamientos si se proporcionaron
            ficha = form.save(commit=True, mascota=paciente, veterinario=request.user, request_data=request.POST)
            
            # Mostrar mensaje de éxito
            messages.success(request, "Ficha clínica creada correctamente.")
            
            # Redirigir a la página de detalle de la ficha recién creada
            return redirect('vet_ficha_detalle', ficha_id=ficha.id)
    else:
        # Si es GET, mostrar formulario vacío para crear nueva ficha
        form = FichaClinicaForm()
    
    # Renderizar template con el formulario
    return render(request, 'gestorUser/veterinario/ficha_form.html', {
        'form': form,                              # Formulario para crear ficha
        'paciente': paciente,                      # Paciente para el que se crea la ficha
        'titulo': f'Crear Ficha Clínica para {paciente.nombre}'  # Título personalizado
    })


@login_required
def vet_ficha_editar(request, ficha_id):
    """Editar ficha clínica existente"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    ficha = get_object_or_404(FichaClinica, id=ficha_id)
    
    if request.method == 'POST':
        form = FichaClinicaForm(request.POST, instance=ficha)
        if form.is_valid():
            # Guardar la ficha clínica junto con múltiples vacunas y tratamientos si se proporcionaron
            ficha = form.save(commit=True, mascota=ficha.mascota, veterinario=request.user, request_data=request.POST)
            messages.success(request, "Ficha clínica actualizada correctamente.")
            return redirect('vet_ficha_detalle', ficha_id=ficha.id)
    else:
        form = FichaClinicaForm(instance=ficha)
    
    return render(request, 'gestorUser/veterinario/ficha_form.html', {
        'form': form,
        'ficha': ficha,
        'paciente': ficha.mascota,
        'titulo': f'Editar Ficha Clínica de {ficha.mascota.nombre}'
    })


# ==================== AGENDA Y CITAS ====================

@login_required
def vet_agenda(request):
    """
    Vista de agenda diaria del veterinario.
    Muestra las citas del día seleccionado y las citas próximas.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # ========== OBTENER FECHA SELECCIONADA ==========
    # Obtener la fecha desde los parámetros GET de la URL
    # Si no se proporciona, usar la fecha actual en formato ISO (YYYY-MM-DD)
    fecha = request.GET.get('fecha', timezone.now().date().isoformat())
    
    # Intentar convertir el string de fecha a objeto date
    try:
        # Convertir string "YYYY-MM-DD" a objeto date
        fecha_obj = timezone.datetime.strptime(fecha, '%Y-%m-%d').date()
    except:
        # Si hay error en el formato, usar la fecha actual como fallback
        fecha_obj = timezone.now().date()
    
    # ========== CITAS DEL DÍA SELECCIONADO ==========
    # Obtener todas las citas médicas para la fecha seleccionada
    # Ordenar por hora (más temprano primero)
    citas_dia = CitaMedica.objects.filter(fecha=fecha_obj).order_by('hora')
    
    # ========== CITAS PRÓXIMAS (PRÓXIMOS 7 DÍAS) ==========
    # Calcular la fecha límite (7 días después del día seleccionado)
    fecha_futuro = fecha_obj + timezone.timedelta(days=7)
    
    # Obtener citas entre el día seleccionado y 7 días después
    # fecha__gte: fecha mayor o igual a fecha_obj
    # fecha__lte: fecha menor o igual a fecha_futuro
    # exclude(fecha=fecha_obj): excluir las citas del día actual (ya están en citas_dia)
    # Ordenar por fecha y hora, limitar a 10 resultados
    citas_proximas = CitaMedica.objects.filter(
        fecha__gte=fecha_obj,      # Desde el día seleccionado
        fecha__lte=fecha_futuro    # Hasta 7 días después
    ).exclude(fecha=fecha_obj).order_by('fecha', 'hora')[:10]
    
    # Renderizar template con la agenda
    return render(request, 'gestorUser/veterinario/agenda.html', {
        'fecha': fecha_obj,        # Fecha del día seleccionado
        'citas_dia': citas_dia,    # Citas del día seleccionado
        'citas_proximas': citas_proximas  # Próximas citas (siguientes 7 días)
    })


@login_required
def vet_citas(request):
    """Listar todas las citas"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    estado = request.GET.get('estado', 'todas')
    citas = CitaMedica.objects.all().order_by('-fecha', '-hora')
    
    if estado == 'pendientes':
        citas = citas.filter(fecha__gte=timezone.now().date())
    elif estado == 'pasadas':
        citas = citas.filter(fecha__lt=timezone.now().date())
    
    return render(request, 'gestorUser/veterinario/citas_lista.html', {
        'citas': citas,
        'estado': estado
    })


@login_required
def vet_cita_detalle(request, cita_id):
    """Ver detalle de una cita"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    cita = get_object_or_404(CitaMedica, id=cita_id)
    
    # Buscar si hay consulta relacionada
    consulta = Consulta.objects.filter(cita=cita).first()
    
    # Buscar mascota relacionada si existe
    mascota = None
    if cita.mascota:
        mascota = Mascota.objects.filter(nombre=cita.mascota, propietario=cita.user).first()
    
    return render(request, 'gestorUser/veterinario/cita_detalle.html', {
        'cita': cita,
        'consulta': consulta,
        'mascota': mascota
    })


# ==================== CONSULTAS MÉDICAS ====================

@login_required
def vet_consultas(request):
    """Listar todas las consultas"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    estado = request.GET.get('estado', 'todas')
    mascota_id = request.GET.get('mascota', None)
    
    consultas = Consulta.objects.select_related('mascota', 'veterinario').order_by('-fecha_consulta')
    
    # Filtrar por mascota si se proporciona
    if mascota_id:
        consultas = consultas.filter(mascota_id=mascota_id)
    
    if estado == 'pendientes':
        consultas = consultas.filter(estado='pendiente')
    elif estado == 'en_proceso':
        consultas = consultas.filter(estado='en_proceso')
    elif estado == 'completadas':
        consultas = consultas.filter(estado='completada')
    
    return render(request, 'gestorUser/veterinario/consultas_lista.html', {
        'consultas': consultas,
        'estado': estado,
        'mascota_filtro': mascota_id  # Para mantener el filtro en el template
    })


@login_required
def vet_consulta_detalle(request, consulta_id):
    """Ver detalle completo de una consulta"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    consulta = get_object_or_404(Consulta, id=consulta_id)
    recetas = Receta.objects.filter(consulta=consulta).prefetch_related('prescripciones')
    
    return render(request, 'gestorUser/veterinario/consulta_detalle.html', {
        'consulta': consulta,
        'recetas': recetas
    })


@login_required
def vet_consulta_crear(request, paciente_id=None, cita_id=None):
    """
    Vista para crear una nueva consulta médica.
    Puede crearse desde un paciente específico o desde una cita médica.
    
    Parámetros opcionales:
    - paciente_id: ID de la mascota para crear consulta directamente
    - cita_id: ID de la cita para convertirla en consulta
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Inicializar variables que pueden venir de diferentes fuentes
    paciente = None  # Mascota a la que se le hará la consulta
    cita = None      # Cita médica relacionada (si existe)
    
    # Determinar de dónde viene la solicitud: desde un paciente o desde una cita
    if 'paciente_id' in request.resolver_match.kwargs:
        # Si viene desde la página de un paciente específico
        paciente_id = request.resolver_match.kwargs.get('paciente_id')
        if paciente_id:
            # Obtener el paciente o devolver 404 si no existe
            paciente = get_object_or_404(Mascota, id=paciente_id)
    elif 'cita_id' in request.resolver_match.kwargs:
        # Si viene desde una cita médica (convertir cita en consulta)
        cita_id = request.resolver_match.kwargs.get('cita_id')
        if cita_id:
            # Obtener la cita médica
            cita = get_object_or_404(CitaMedica, id=cita_id)
            # Intentar encontrar la mascota relacionada con la cita
            # La cita tiene el nombre de la mascota como string, buscamos el objeto Mascota
            if cita.mascota:
                paciente = Mascota.objects.filter(
                    nombre=cita.mascota,  # Nombre de la mascota en la cita
                    propietario=cita.user  # Mismo propietario que la cita
                ).first()  # first() devuelve None si no encuentra
    
    # Procesar formulario si se envió (POST)
    if request.method == 'POST':
        # Crear formulario con los datos enviados
        form = ConsultaForm(request.POST)
        if form.is_valid():
            # Guardar sin commit para poder agregar información adicional
            consulta = form.save(commit=False)
            
            # Asignar el veterinario actual como responsable de la consulta
            consulta.veterinario = request.user
            
            # Asignar la mascota si fue proporcionada (desde paciente o cita)
            if paciente:
                consulta.mascota = paciente
            
            # Vincular la consulta con la cita si viene de una cita
            if cita:
                consulta.cita = cita  # Relaciona la consulta con la cita original
            
            # Guardar la consulta en la base de datos
            consulta.save()
            
            # Mostrar mensaje de éxito
            messages.success(request, "Consulta creada correctamente.")
            
            # Redirigir a la página de detalle de la consulta recién creada
            return redirect('vet_consulta_detalle', consulta_id=consulta.id)
    else:
        # Si es GET, mostrar formulario para crear nueva consulta
        form = ConsultaForm()
        
        # Si hay un paciente, preseleccionarlo en el formulario
        if paciente:
            form.fields['mascota'].initial = paciente
    
    # Renderizar template con el formulario
    return render(request, 'gestorUser/veterinario/consulta_form.html', {
        'form': form,                    # Formulario para crear consulta
        'paciente': paciente,            # Paciente preseleccionado (si aplica)
        'cita': cita,                    # Cita relacionada (si aplica)
        'titulo': 'Crear Nueva Consulta' # Título para el template
    })


@login_required
def vet_consulta_editar(request, consulta_id):
    """Editar consulta existente"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.veterinario = request.user
            consulta.save()
            messages.success(request, "Consulta actualizada correctamente.")
            return redirect('vet_consulta_detalle', consulta_id=consulta.id)
    else:
        form = ConsultaForm(instance=consulta)
    
    return render(request, 'gestorUser/veterinario/consulta_form.html', {
        'form': form,
        'consulta': consulta,
        'titulo': f'Editar Consulta - {consulta.mascota.nombre}'
    })


@login_required
def vet_consulta_completar(request, consulta_id):
    """Marcar consulta como completada"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    consulta = get_object_or_404(Consulta, id=consulta_id)
    consulta.estado = 'completada'
    consulta.save()
    messages.success(request, "Consulta marcada como completada.")
    return redirect('vet_consulta_detalle', consulta_id=consulta.id)


# ==================== RECETAS Y PRESCRIPCIONES ====================

@login_required
def vet_recetas(request):
    """Listar todas las recetas"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    recetas = Receta.objects.select_related('consulta', 'veterinario').order_by('-fecha_emision')
    
    return render(request, 'gestorUser/veterinario/recetas_lista.html', {
        'recetas': recetas
    })


@login_required
def vet_receta_detalle(request, receta_id):
    """Ver detalle de una receta"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    receta = get_object_or_404(Receta, id=receta_id)
    prescripciones = Prescripcion.objects.filter(receta=receta)
    
    return render(request, 'gestorUser/veterinario/receta_detalle.html', {
        'receta': receta,
        'prescripciones': prescripciones
    })


@login_required
def vet_receta_crear(request, consulta_id):
    """
    Vista para crear una nueva receta médica asociada a una consulta.
    La receta se crea primero y luego se pueden agregar prescripciones de medicamentos.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Obtener la consulta a la que se asociará la receta
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Procesar formulario si se envió (POST)
    if request.method == 'POST':
        # Crear formulario con los datos enviados
        form = RecetaForm(request.POST)
        if form.is_valid():
            # Guardar sin commit para agregar información adicional
            receta = form.save(commit=False)
            
            # Asignar la consulta a la que pertenece esta receta
            receta.consulta = consulta
            
            # Asignar el veterinario actual como emisor de la receta
            receta.veterinario = request.user
            
            # Guardar la receta en la base de datos
            receta.save()
            
            # Mostrar mensaje informando que ahora se pueden agregar prescripciones
            messages.success(request, "Receta creada correctamente. Ahora puedes agregar prescripciones.")
            
            # Redirigir a la página de detalle de la receta para agregar prescripciones
            return redirect('vet_receta_detalle', receta_id=receta.id)
    else:
        # Si es GET, mostrar formulario vacío para crear nueva receta
        form = RecetaForm()
    
    # Renderizar template con el formulario
    return render(request, 'gestorUser/veterinario/receta_form.html', {
        'form': form,                                    # Formulario para crear receta
        'consulta': consulta,                            # Consulta relacionada
        'titulo': f'Crear Receta para {consulta.mascota.nombre}'  # Título personalizado
    })


@login_required
def vet_prescripcion_agregar(request, receta_id):
    """
    Vista para agregar una prescripción (medicamento) a una receta existente.
    Una receta puede tener múltiples prescripciones (varios medicamentos).
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Obtener la receta a la que se agregará la prescripción
    receta = get_object_or_404(Receta, id=receta_id)
    
    # Procesar formulario si se envió (POST)
    if request.method == 'POST':
        # Crear formulario con los datos del medicamento prescrito
        form = PrescripcionForm(request.POST)
        if form.is_valid():
            # Guardar sin commit para asignar la receta
            prescripcion = form.save(commit=False)
            
            # Asignar la receta a la que pertenece esta prescripción
            prescripcion.receta = receta
            
            # Guardar la prescripción en la base de datos
            prescripcion.save()
            
            # Mostrar mensaje de éxito
            messages.success(request, "Prescripción agregada correctamente.")
            
            # Redirigir a la página de detalle de la receta para ver todas las prescripciones
            return redirect('vet_receta_detalle', receta_id=receta.id)
    else:
        # Si es GET, mostrar formulario vacío para agregar nueva prescripción
        form = PrescripcionForm()
    
    # Renderizar template con el formulario
    return render(request, 'gestorUser/veterinario/prescripcion_form.html', {
        'form': form,       # Formulario para agregar prescripción
        'receta': receta    # Receta a la que se agregará la prescripción
    })


# ==================== VACUNAS ====================

@login_required
def vet_vacunas(request, paciente_id=None):
    """
    Vista para listar vacunas.
    Puede mostrar todas las vacunas o solo las de un paciente específico.
    
    Parámetros:
        paciente_id (opcional): ID del paciente para filtrar vacunas
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Si se proporciona paciente_id, mostrar solo vacunas de ese paciente
    if paciente_id:
        # Obtener el paciente por su ID
        paciente = get_object_or_404(Mascota, id=paciente_id)
        
        # Obtener todas las vacunas de ese paciente
        # Ordenar por fecha de aplicación descendente (más recientes primero)
        vacunas = Vacuna.objects.filter(
            mascota=paciente
        ).order_by('-fecha_aplicacion')
    else:
        # Si no hay paciente_id, mostrar todas las vacunas del sistema
        # select_related optimiza la consulta trayendo mascota y veterinario
        vacunas = Vacuna.objects.select_related(
            'mascota',      # Datos de la mascota vacunada
            'veterinario'   # Datos del veterinario que aplicó
        ).order_by('-fecha_aplicacion')
        paciente = None  # No hay paciente específico
    
    # Renderizar template con la lista de vacunas
    return render(request, 'gestorUser/veterinario/vacunas_lista.html', {
        'vacunas': vacunas,  # Lista de vacunas (filtradas o todas)
        'paciente': paciente # Paciente específico (si aplica)
    })


@login_required
def vet_vacuna_registrar(request, paciente_id):
    """Registrar nueva vacuna"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    paciente = get_object_or_404(Mascota, id=paciente_id)
    
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            vacuna = form.save(commit=False)
            vacuna.mascota = paciente
            vacuna.veterinario = request.user
            vacuna.save()
            messages.success(request, "Vacuna registrada correctamente.")
            return redirect('vet_vacunas', paciente_id=paciente.id)
    else:
        form = VacunaForm()
    
    return render(request, 'gestorUser/veterinario/vacuna_form.html', {
        'form': form,
        'paciente': paciente
    })


# ==================== TRATAMIENTOS ====================

@login_required
def vet_tratamientos(request, paciente_id=None):
    """Listar tratamientos (por paciente o todos)"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    if paciente_id:
        paciente = get_object_or_404(Mascota, id=paciente_id)
        tratamientos = Tratamiento.objects.filter(mascota=paciente).order_by('-fecha_inicio')
    else:
        tratamientos = Tratamiento.objects.select_related('mascota', 'veterinario').order_by('-fecha_inicio')
        paciente = None
    
    return render(request, 'gestorUser/veterinario/tratamientos_lista.html', {
        'tratamientos': tratamientos,
        'paciente': paciente
    })


@login_required
def vet_tratamiento_registrar(request, paciente_id):
    """Registrar nuevo tratamiento"""
    check = verificar_veterinario(request)
    if check:
        return check
    
    paciente = get_object_or_404(Mascota, id=paciente_id)
    
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.mascota = paciente
            tratamiento.veterinario = request.user
            tratamiento.save()
            messages.success(request, "Tratamiento registrado correctamente.")
            return redirect('vet_tratamientos', paciente_id=paciente.id)
    else:
        form = TratamientoForm()
    
    return render(request, 'gestorUser/veterinario/tratamiento_form.html', {
        'form': form,
        'paciente': paciente
    })


# ==================== INVENTARIO MÉDICO ====================

@login_required
def vet_inventario(request):
    """
    Vista para ver el inventario completo de todos los productos.
    Muestra todos los productos (medicamentos, alimentos, accesorios, etc.)
    ordenados alfabéticamente con sus stocks disponibles.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # ========== OBTENER TODOS LOS PRODUCTOS AGRUPADOS POR CATEGORÍA ==========
    # Diccionario para almacenar productos agrupados por categoría
    productos_por_categoria = {}
    
    # Función helper para normalizar productos y agregarlos a su categoría
    def agregar_productos(queryset, tipo_producto):
        """Agrega productos del queryset a la categoría correspondiente"""
        if queryset.count() == 0:
            return  # No agregar categorías vacías
        
        productos_categoria = []
        for producto in queryset:
            # Normalizar precio (algunos son Integer, otros DecimalField)
            precio = float(producto.precio)
            
            # Normalizar descripción (algunos son CharField, otros TextField)
            descripcion = getattr(producto, 'descripcion', '')
            if not descripcion:
                descripcion = getattr(producto, 'marca', '')
            
            # Obtener marca si existe
            marca = getattr(producto, 'marca', '')
            
            productos_categoria.append({
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'marca': marca,
                'descripcion': descripcion,
                'precio': precio,
                'stock': producto.stock,
                'tipo': tipo_producto,
                'objeto': producto  # Guardar referencia al objeto original
            })
        
        # Ordenar productos de esta categoría alfabéticamente por nombre
        productos_categoria.sort(key=lambda x: x['nombre'].lower())
        productos_por_categoria[tipo_producto] = productos_categoria
    
    # Obtener todos los productos de cada modelo y agregarlos agrupados por categoría
    agregar_productos(Medicamento.objects.all(), 'Medicamento')
    agregar_productos(Antiparasitario.objects.all(), 'Antiparasitario')
    agregar_productos(Productos.objects.all(), 'Producto General')
    agregar_productos(PCProductos.objects.all(), 'Alimento Perro Cachorro')
    agregar_productos(PAProductos.objects.all(), 'Alimento Perro Adulto')
    agregar_productos(PSProductos.objects.all(), 'Alimento Perro Senior')
    agregar_productos(AProductos.objects.all(), 'Alimento General')
    agregar_productos(AGAProductos.objects.all(), 'Alimento Gato Adulto')
    agregar_productos(AGCProductos.objects.all(), 'Alimento Gato Cachorro')
    agregar_productos(SnackGProductos.objects.all(), 'Snack Gato')
    agregar_productos(SnackPProductos.objects.all(), 'Snack Perro')
    agregar_productos(Shampoo.objects.all(), 'Shampoo')
    agregar_productos(Cama.objects.all(), 'Cama')
    agregar_productos(Collar.objects.all(), 'Collar')
    agregar_productos(Juguete.objects.all(), 'Juguete')
    
    # Crear lista plana de todos los productos para estadísticas
    todos_los_productos = []
    for categoria, productos in productos_por_categoria.items():
        todos_los_productos.extend(productos)
    
    # ========== CALCULAR ESTADÍSTICAS DEL INVENTARIO ==========
    total_productos = len(todos_los_productos)
    total_stock = sum(p['stock'] for p in todos_los_productos)
    
    # Contar productos por nivel de stock
    productos_criticos = sum(1 for p in todos_los_productos if p['stock'] < 10)
    productos_bajos = sum(1 for p in todos_los_productos if 10 <= p['stock'] < 20)
    productos_normales = sum(1 for p in todos_los_productos if p['stock'] >= 20)
    
    # Renderizar template con el inventario agrupado por categoría y estadísticas
    return render(request, 'gestorUser/veterinario/inventario.html', {
        'productos_por_categoria': productos_por_categoria,  # Diccionario de categorías con sus productos
        'total_productos': total_productos,                  # Total de productos diferentes
        'total_stock': total_stock,                          # Suma total de unidades en stock
        'productos_criticos': productos_criticos,            # Productos con stock < 10
        'productos_bajos': productos_bajos,                  # Productos con stock 10-19
        'productos_normales': productos_normales             # Productos con stock >= 20
    })


@login_required
def vet_inventario_alertas(request):
    """
    Vista para ver alertas de productos con stock bajo o crítico.
    Muestra solo productos con stock menor a 20 unidades (críticos < 10 y bajos 10-19),
    agrupados por categoría para facilitar la visualización rápida.
    """
    # Verificar permisos de veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # ========== OBTENER PRODUCTOS CON STOCK BAJO O CRÍTICO AGRUPADOS POR CATEGORÍA ==========
    # Diccionario para almacenar productos agrupados por categoría
    productos_por_categoria = {}
    
    # Función helper para normalizar productos y agregarlos a su categoría
    # Solo incluye productos con stock < 20 (críticos < 10 o bajos 10-19)
    def agregar_productos_alertas(queryset, tipo_producto):
        """Agrega productos del queryset que tengan stock < 20 a la categoría correspondiente"""
        # Filtrar solo productos con stock menor a 20
        productos_filtrados = queryset.filter(stock__lt=20)
        
        if productos_filtrados.count() == 0:
            return  # No agregar categorías vacías
        
        productos_categoria = []
        for producto in productos_filtrados:
            # Normalizar precio (algunos son Integer, otros DecimalField)
            precio = float(producto.precio)
            
            # Normalizar descripción (algunos son CharField, otros TextField)
            descripcion = getattr(producto, 'descripcion', '')
            if not descripcion:
                descripcion = getattr(producto, 'marca', '')
            
            # Obtener marca si existe
            marca = getattr(producto, 'marca', '')
            
            productos_categoria.append({
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'marca': marca,
                'descripcion': descripcion,
                'precio': precio,
                'stock': producto.stock,
                'tipo': tipo_producto,
                'objeto': producto  # Guardar referencia al objeto original
            })
        
        # Ordenar productos de esta categoría por stock ascendente (los más críticos primero)
        # y luego alfabéticamente por nombre
        productos_categoria.sort(key=lambda x: (x['stock'], x['nombre'].lower()))
        productos_por_categoria[tipo_producto] = productos_categoria
    
    # Obtener todos los productos con stock bajo o crítico de cada modelo
    agregar_productos_alertas(Medicamento.objects.all(), 'Medicamento')
    agregar_productos_alertas(Antiparasitario.objects.all(), 'Antiparasitario')
    agregar_productos_alertas(Productos.objects.all(), 'Producto General')
    agregar_productos_alertas(PCProductos.objects.all(), 'Alimento Perro Cachorro')
    agregar_productos_alertas(PAProductos.objects.all(), 'Alimento Perro Adulto')
    agregar_productos_alertas(PSProductos.objects.all(), 'Alimento Perro Senior')
    agregar_productos_alertas(AProductos.objects.all(), 'Alimento General')
    agregar_productos_alertas(AGAProductos.objects.all(), 'Alimento Gato Adulto')
    agregar_productos_alertas(AGCProductos.objects.all(), 'Alimento Gato Cachorro')
    agregar_productos_alertas(SnackGProductos.objects.all(), 'Snack Gato')
    agregar_productos_alertas(SnackPProductos.objects.all(), 'Snack Perro')
    agregar_productos_alertas(Shampoo.objects.all(), 'Shampoo')
    agregar_productos_alertas(Cama.objects.all(), 'Cama')
    agregar_productos_alertas(Collar.objects.all(), 'Collar')
    agregar_productos_alertas(Juguete.objects.all(), 'Juguete')
    
    # Crear lista plana de todos los productos con alertas para estadísticas
    todos_los_productos = []
    for categoria, productos in productos_por_categoria.items():
        todos_los_productos.extend(productos)
    
    # ========== CALCULAR ESTADÍSTICAS DE ALERTAS ==========
    total_productos_alertas = len(todos_los_productos)
    productos_criticos = sum(1 for p in todos_los_productos if p['stock'] < 10)
    productos_bajos = sum(1 for p in todos_los_productos if 10 <= p['stock'] < 20)
    
    # Renderizar template con las alertas agrupadas por categoría
    return render(request, 'gestorUser/veterinario/inventario_alertas.html', {
        'productos_por_categoria': productos_por_categoria,  # Diccionario de categorías con productos en alerta
        'total_productos_alertas': total_productos_alertas,  # Total de productos con stock bajo/crítico
        'productos_criticos': productos_criticos,            # Productos con stock < 10
        'productos_bajos': productos_bajos                   # Productos con stock 10-19
    })


@login_required
def vet_egreso_registrar(request):
    """
    Vista para registrar el egreso (salida) de medicamentos del inventario.
    Cuando se registra un egreso, se actualiza automáticamente el stock del medicamento.
    """
    # Verificar que el usuario es veterinario
    check = verificar_veterinario(request)
    if check:
        return check
    
    # Procesar formulario si se envió (POST)
    if request.method == 'POST':
        # Crear formulario con los datos enviados
        form = EgresoMedicamentoForm(request.POST)
        if form.is_valid():
            # Guardar sin commit para poder agregar información adicional
            egreso = form.save(commit=False)
            
            # Asignar el veterinario actual como responsable del egreso
            egreso.veterinario = request.user
            
            # ========== ACTUALIZAR STOCK DEL MEDICAMENTO ==========
            # Obtener el nombre del medicamento del formulario
            medicamento_nombre = egreso.medicamento
            
            # Buscar el medicamento en el inventario por nombre (búsqueda parcial)
            # first() devuelve el primer resultado o None si no encuentra
            medicamento = Medicamento.objects.filter(
                nombre__icontains=medicamento_nombre
            ).first()
            
            if medicamento:
                # Si el medicamento existe en el inventario, verificar stock disponible
                if medicamento.stock >= egreso.cantidad:
                    # Si hay stock suficiente, restar la cantidad egresada
                    medicamento.stock -= egreso.cantidad
                    medicamento.save()  # Guardar el nuevo stock
                    
                    # Guardar el registro de egreso
                    egreso.save()
                    
                    # Mostrar mensaje de éxito indicando que se actualizó el stock
                    messages.success(
                        request, 
                        "Egreso registrado y stock actualizado correctamente."
                    )
                else:
                    # Si no hay stock suficiente, mostrar error y no guardar
                    messages.error(
                        request, 
                        f"Stock insuficiente. Stock disponible: {medicamento.stock}"
                    )
                    # Volver a mostrar el formulario con el error (sin guardar)
                    return render(
                        request, 
                        'gestorUser/veterinario/egreso_form.html', 
                        {'form': form}
                    )
            else:
                # Si el medicamento no está en el inventario, guardar el egreso igual
                # pero sin actualizar stock (medicamento externo o no registrado)
                egreso.save()
                messages.success(request, "Egreso registrado correctamente.")
            
            # Redirigir a la vista de inventario después de guardar
            return redirect('vet_inventario')
    else:
        # Si es GET, mostrar formulario vacío para registrar nuevo egreso
        form = EgresoMedicamentoForm()
    
    # Renderizar template con el formulario
    return render(request, 'gestorUser/veterinario/egreso_form.html', {
        'form': form  # Formulario para registrar egreso
    })

