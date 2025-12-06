from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import VeterinarioProfile

@login_required
def vet_veterinario(request):
    """
    Vista del dashboard principal para veterinarios.
    Muestra estadísticas, consultas recientes y citas próximas.
    """
    # ========== VERIFICACIÓN DE PERMISOS ==========
    # Verificar que el usuario tiene perfil de veterinario activo
    es_vet = False
    try:
        # Intentar obtener el perfil de veterinario del usuario
        perfil = VeterinarioProfile.objects.get(user=request.user)
        es_vet = perfil.es_veterinario  # True solo si está activado
    except VeterinarioProfile.DoesNotExist:
        # Si no tiene perfil, no es veterinario
        es_vet = False
    
    # Si NO es veterinario, redirigir a vista de cliente con mensaje de advertencia
    if not es_vet:
        from django.contrib import messages
        messages.warning(request, "No tienes permisos para acceder al panel de veterinario.")
        return redirect('vet_inicio')  # Redirigir a vista de cliente
    
    # ========== CARGAR DATOS DEL DASHBOARD ==========
    # Importar modelos y utilidades necesarias
    from .models import Mascota, Consulta, CitaMedica, Receta
    from django.db.models import Count, Q
    from django.utils import timezone
    
    # ========== CALCULAR ESTADÍSTICAS ==========
    # Total de pacientes activos en el sistema
    total_pacientes = Mascota.objects.filter(activa=True).count()
    
    # Consultas realizadas hoy (filtrando por fecha de consulta)
    # fecha_consulta__date: compara solo la fecha (sin hora) con la fecha actual
    consultas_hoy = Consulta.objects.filter(
        fecha_consulta__date=timezone.now().date()
    ).count()
    
    # Consultas pendientes de atender (estado='pendiente')
    consultas_pendientes = Consulta.objects.filter(estado='pendiente').count()
    
    # Citas médicas agendadas para hoy
    citas_hoy = CitaMedica.objects.filter(
        fecha=timezone.now().date()
    ).count()
    
    # Últimas 5 consultas realizadas (más recientes primero)
    # select_related optimiza la consulta trayendo la mascota en la misma query
    consultas_recientes = Consulta.objects.select_related('mascota').order_by(
        '-fecha_consulta'  # Orden descendente (más recientes primero)
    )[:5]  # Limitar a 5 resultados
    
    # Próximas 5 citas médicas (fecha mayor o igual a hoy, ordenadas por fecha y hora)
    citas_proximas = CitaMedica.objects.filter(
        fecha__gte=timezone.now().date()  # fecha mayor o igual a hoy
    ).order_by('fecha', 'hora')[:5]  # Ordenar por fecha y hora, limitar a 5
    
    # Renderizar template del dashboard con todas las estadísticas
    return render(request, 'gestorUser/veterinario/dashboard.html', {
        'total_pacientes': total_pacientes,          # Total de pacientes activos
        'consultas_hoy': consultas_hoy,              # Consultas del día
        'consultas_pendientes': consultas_pendientes, # Consultas sin atender
        'citas_hoy': citas_hoy,                      # Citas del día
        'consultas_recientes': consultas_recientes,  # Últimas consultas
        'citas_proximas': citas_proximas,            # Próximas citas
    })


@login_required
def vetInicio(request):
    """
    Vista de inicio para clientes - Muestra productos, carrito y formulario de citas.
    
    Esta función es dinámica y verifica el tipo de usuario:
    - Si es VETERINARIO: Redirige a su dashboard (vet_veterinario)
    - Si es CLIENTE: Muestra la vista de productos y carrito
    
    IMPORTANTE: Esta función fue modificada para diferenciar entre veterinarios
    y clientes. Los veterinarios tienen su propia vista en el sistema de veterinario.
    
    Parámetros:
        request: HttpRequest con el usuario autenticado
        
    Retorna:
        HttpResponse: 
        - Redirect a 'vet_veterinario' si es veterinario
        - Render de 'vetInicio.html' con productos y formulario de citas si es cliente
        
    Contexto enviado al template:
        - productos: Lista de productos (primeros 20)
        - formulario_cita: Instancia del formulario para agendar citas
        - citas_usuario: Lista de citas agendadas por el usuario
    """
    # ========== VERIFICACIÓN DE TIPO DE USUARIO ==========
    # Verificar si el usuario es veterinario mediante su perfil
    es_vet = False
    try:
        # Intentar obtener el perfil de veterinario del usuario
        perfil = VeterinarioProfile.objects.get(user=request.user)
        es_vet = perfil.es_veterinario  # True si está activado como veterinario
    except VeterinarioProfile.DoesNotExist:
        # Si no tiene perfil, definitivamente no es veterinario
        es_vet = False
    
    # ========== REDIRECCIÓN PARA VETERINARIOS ==========
    # Si es veterinario, redirigir a su dashboard específico
    if es_vet:
        return redirect('vet_veterinario')  # URL: /vet_veterinario/
    
    # ========== VISTA PARA CLIENTES ==========
    # Importar modelos y formularios necesarios para la vista de cliente
    from gestorProductos.models import Productos
    from gestorUser.models import CitaMedica
    from gestorUser.forms import CitaMedicaForm
    
    # Obtener productos para mostrar (primeros 20)
    productos = Productos.objects.all()[:20]
    
    # Inicializar variables para el formulario de citas
    citas_usuario = []
    formulario_cita = CitaMedicaForm()  # Formulario vacío para nueva cita
    
    # Si el usuario está autenticado, obtener sus citas agendadas
    if request.user.is_authenticated:
        citas_usuario = CitaMedica.objects.filter(
            user=request.user
        ).order_by('fecha', 'hora')
    
    # Renderizar template con el contexto necesario
    return render(request, 'gestorProductos/vetInicio.html', {
        'productos': productos,           # Lista de productos disponibles
        'formulario_cita': formulario_cita,  # Formulario para agendar citas
        'citas_usuario': citas_usuario,   # Citas ya agendadas por el usuario
    })

def index(request):
    if request.user.is_authenticated:
        # Solo superusuarios y staff pueden acceder al dashboard
        # Veterinarios → vet_veterinario, Clientes → vet_inicio
        if not (request.user.is_superuser or request.user.is_staff):
            # Verificar si es veterinario
            es_vet = False
            try:
                perfil = VeterinarioProfile.objects.get(user=request.user)
                es_vet = perfil.es_veterinario
            except VeterinarioProfile.DoesNotExist:
                es_vet = False
            
            if es_vet:
                return redirect('vet_veterinario')
            else:
                return redirect('vet_inicio')
    # Importar la vista home de gestorProductos para obtener los datos
    from gestorProductos.views import home
    return home(request)  # Usa la vista home que tiene toda la lógica de datos

def login_redirect(request):
    """
    Función central de redirección después del login.
    
    Esta función determina a qué vista debe ir cada usuario después de iniciar sesión,
    basándose en su rol y permisos:
    
    Flujo de redirección:
    1. Superusuarios/Staff → Dashboard de administración (/index)
    2. Veterinarios → Dashboard de veterinario (/vet_veterinario)
    3. Clientes → Vista de productos y carrito (/vet_inicio)
    
    Esta función es llamada automáticamente después del login gracias a la
    configuración en settings.py: LOGIN_REDIRECT_URL = 'login_redirect'
    
    Parámetros:
        request: HttpRequest con el usuario ya autenticado
        
    Retorna:
        HttpResponseRedirect: Redirección a la vista correspondiente según el rol
        
    Notas:
        - Verifica primero si es admin/staff (mayor prioridad)
        - Luego verifica si es veterinario mediante VeterinarioProfile
        - Por defecto, trata al usuario como cliente
    """
    # ========== PRIORIDAD 1: ADMINISTRADORES ==========
    # Los superusuarios y staff van directamente al dashboard de administración
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_index')  # URL: /index
    
    # ========== PRIORIDAD 2: VETERINARIOS ==========
    # Verificar si el usuario tiene perfil de veterinario activo
    es_veterinario = False
    try:
        # Acceder a la relación OneToOne (si no existe, lanza DoesNotExist)
        perfil = request.user.veterinarioprofile
        es_veterinario = perfil.es_veterinario  # True solo si está activado
    except VeterinarioProfile.DoesNotExist:
        # Si no tiene perfil de veterinario, no es veterinario
        es_veterinario = False
    
    # Si es veterinario, redirigir a su dashboard
    if es_veterinario:
        return redirect('vet_veterinario')  # URL: /vet_veterinario/
    
    # ========== PRIORIDAD 3: CLIENTES ==========
    # Por defecto, todos los demás usuarios son clientes
    # Los clientes ven la página de productos, carrito y pueden agendar citas
    return redirect('vet_inicio')  # URL: /vet_inicio/

class SignUpView(SuccessMessageMixin,CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = "¡Usuario creado exitosamente!"

    def form_valid(self, form):
        response = super().form_valid(form)
        es_veterinario = form.cleaned_data.get('es_veterinario', False)
        VeterinarioProfile.objects.create(user=self.object, es_veterinario=es_veterinario)
        return response

# List all admins (users with is_staff=True)
class AdminListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'gestorUser/admin_list.html'
    context_object_name = 'admins'

    def get_queryset(self):
        return User.objects.filter(is_staff=True)

# List all clients (users who are not staff or veterinario)
class ClientListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'gestorUser/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        veterinarios = VeterinarioProfile.objects.filter(es_veterinario=True).values_list('user_id', flat=True)
        return User.objects.filter(is_staff=False).exclude(id__in=veterinarios)

# List all veterinarians
class VeterinarioListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'gestorUser/veterinario_list.html'
    context_object_name = 'veterinarios'

    def get_queryset(self):
        veterinarios = VeterinarioProfile.objects.filter(es_veterinario=True).values_list('user_id', flat=True)
        return User.objects.filter(id__in=veterinarios)

# Create views for Admin, Client, Veterinario - reuse SignUpView but with role preset
class AdminCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('admin_list')
    success_message = "Administrador creado exitosamente."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_staff = True
        user.save()
        return response

class ClientCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('client_list')
    success_message = "Cliente creado exitosamente."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        # Ensure client is not staff and not veterinarian
        user.is_staff = False
        user.is_superuser = False
        # Remove VeterinarioProfile if exists
        try:
            profile = user.veterinarioprofile
            profile.delete()
        except VeterinarioProfile.DoesNotExist:
            pass
        user.save()
        return response

class VeterinarioCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('veterinario_list')
    success_message = "Veterinario creado exitosamente."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_staff = False
        user.is_superuser = False
        es_veterinario = form.cleaned_data.get('es_veterinario', False)
        VeterinarioProfile.objects.update_or_create(user=user, defaults={'es_veterinario': es_veterinario})
        user.save()
        return response

# Update views (reuse CustomUserChangeForm to handle roles and profile)
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'gestorUser/user_form.html'
    success_url = reverse_lazy('index')
    success_message = "Usuario actualizado exitosamente."

    def get_success_url(self):
        # Redirect based on user role
        user = self.object
        if user.is_staff:
            return reverse_lazy('admin_list')
        else:
            try:
                perfil = user.veterinarioprofile
                if perfil.es_veterinario:
                    return reverse_lazy('veterinario_list')
            except VeterinarioProfile.DoesNotExist:
                pass
            return reverse_lazy('client_list')

# Delete view for users
class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'gestorUser/user_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        user = self.object
        if user.is_staff:
            return reverse_lazy('admin_list')
        else:
            try:
                perfil = user.veterinarioprofile
                if perfil.es_veterinario:
                    return reverse_lazy('veterinario_list')
            except VeterinarioProfile.DoesNotExist:
                pass
            return reverse_lazy('client_list')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import (
    CitaMedica, VeterinarioProfile, Mascota, FichaClinica, Consulta,
    Receta, Prescripcion, Vacuna, Tratamiento, EgresoMedicamento
)
from .forms import (
    CitaMedicaForm, VeterinarioProfileForm, MascotaForm, FichaClinicaForm,
    ConsultaForm, RecetaForm, PrescripcionForm, VacunaForm, TratamientoForm,
    EgresoMedicamentoForm
)
from django.utils import timezone
from django.db.models import Q, Sum
from gestorProductos.models import Medicamento, Antiparasitario

@login_required
def gestionar_citas(request):
    citas = CitaMedica.objects.filter(user=request.user).order_by('fecha', 'hora')
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.user = request.user
            try:
                cita.full_clean()  # Model validation to prevent conflicts
                cita.save()
                messages.success(request, "Cita agendada correctamente.")
                return redirect('vet_inicio')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CitaMedicaForm()
    return render(request, 'gestorProductos/vetInicio.html', {'formulario_cita': form, 'citas_usuario': citas})


@login_required
def agendar_cita(request):
    """
    Vista para que los clientes agenden citas médicas.
    
    Esta función maneja el formulario mejorado de agendamiento de citas con
    todas sus validaciones. Los clientes pueden:
    - Agendar nuevas citas
    - Ver sus citas agendadas
    - Recibir mensajes claros sobre errores de validación
    
    Validaciones implementadas:
    - Fecha no puede ser en el pasado
    - Horario de atención (09:00 - 18:00)
    - No permite citas duplicadas (misma fecha y hora)
    - Campos obligatorios validados
    
    Parámetros:
        request: HttpRequest con el usuario autenticado
        
    Retorna:
        HttpResponse: 
        - Si POST y válido: Redirect a la misma página con mensaje de éxito
        - Si POST y con errores: Render con formulario y errores
        - Si GET: Render con formulario vacío y lista de citas
        
    Contexto enviado al template:
        - formulario_cita: Instancia del formulario (vacío o con datos/errores)
        - citas_usuario: Lista de citas agendadas por el usuario actual
    """
    # Obtener todas las citas del usuario actual ordenadas por fecha y hora
    citas = CitaMedica.objects.filter(
        user=request.user
    ).order_by('fecha', 'hora')
    
    # ========== PROCESAMIENTO DE FORMULARIO (POST) ==========
    if request.method == 'POST':
        # Crear instancia del formulario con los datos enviados
        form = CitaMedicaForm(request.POST)
        
        if form.is_valid():
            # Guardar sin commit para poder modificar antes de guardar en BD
            cita = form.save(commit=False)
            cita.user = request.user  # Asignar el usuario actual como propietario de la cita
            
            # ========== AUTO-COMPLETAR TITULAR ==========
            # Si el usuario no especificó un titular, usar su nombre completo o username
            if not cita.titular:
                cita.titular = request.user.get_full_name() or request.user.username
            
            # ========== VALIDACIÓN ADICIONAL DEL MODELO ==========
            try:
                # Ejecutar validaciones del modelo (clean())
                # Esto verifica: fechas pasadas, citas duplicadas, etc.
                cita.full_clean()
                cita.save()  # Guardar en la base de datos
                
                # Mensaje de éxito con información de la cita
                messages.success(
                    request, 
                    f"¡Cita agendada correctamente para {cita.mascota} el {cita.fecha} a las {cita.hora.strftime('%H:%M')}!"
                )
                return redirect('agendar_cita')  # Recargar la página para mostrar mensaje
                
            except ValidationError as e:
                # ========== MANEJO DE ERRORES DE VALIDACIÓN ==========
                # Si hay errores de validación del modelo, agregarlos al formulario
                if hasattr(e, 'error_dict'):
                    # Si el error tiene estructura de diccionario (errores por campo)
                    for field, errors in e.error_dict.items():
                        for error in errors:
                            form.add_error(field, error)
                else:
                    # Si es un error general, mostrarlo como mensaje
                    messages.error(request, f"Error al agendar la cita: {str(e)}")
                    
            except Exception as e:
                # ========== MANEJO DE ERRORES INESPERADOS ==========
                # Capturar cualquier otro error no previsto
                messages.error(request, f"Error inesperado: {str(e)}")
    else:
        # ========== MOSTRAR FORMULARIO VACÍO (GET) ==========
        form = CitaMedicaForm()

    # Renderizar template con el formulario y la lista de citas
    return render(request, 'gestorUser/agendar_cita.html', {
        'formulario_cita': form,      # Formulario (vacío o con datos/errores)
        'citas_usuario': citas        # Lista de citas ya agendadas
    })


# ==================== IMPORTAR VISTAS DEL SISTEMA DE VETERINARIO ====================
from .veterinario_views import *

