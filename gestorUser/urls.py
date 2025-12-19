from django.urls import path
from gestorUser.views import (
    SignUpView,
    AdminListView, AdminCreateView,
    ClientListView, ClientCreateView,
    VeterinarioListView, VeterinarioCreateView,
    UserUpdateView, UserDeleteView,
    gestionar_citas,
    agendar_cita,
    obtener_horas_disponibles,
    # Vistas del sistema de veterinario
    vet_perfil, vet_pacientes, vet_paciente_detalle, vet_paciente_crear, vet_paciente_editar,
    vet_fichas_clinicas, vet_ficha_detalle, vet_ficha_crear, vet_ficha_editar,
    vet_agenda, vet_agenda_api, vet_citas, vet_cita_detalle, vet_cita_eliminar,
    vet_consultas, vet_consulta_detalle, vet_consulta_crear, vet_consulta_crear_ajax, vet_consulta_editar, vet_consulta_completar,
    vet_mascota_crear_ajax,
    vet_recetas, vet_receta_detalle, vet_receta_crear, vet_prescripcion_agregar,
    vet_vacunas, vet_vacuna_registrar,
    vet_tratamientos, vet_tratamiento_registrar,
    vet_inventario, vet_inventario_alertas, vet_egreso_registrar,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="Signup"),

    # Admin user urls
    path('admin/list/', AdminListView.as_view(), name='admin_list'),
    path('admin/create/', AdminCreateView.as_view(), name='admin_create'),

    # Client user urls
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),

    # Veterinario user urls
    path('veterinario/list/', VeterinarioListView.as_view(), name='veterinario_list'),
    path('veterinario/create/', VeterinarioCreateView.as_view(), name='veterinario_create'),

    # Generic update and delete urls for users (all roles)
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    # Appointment scheduling
    path('citas/', gestionar_citas, name='gestionar_citas'),
    path('citas/agendar/', agendar_cita, name='agendar_cita'),
    path('citas/horas-disponibles/', obtener_horas_disponibles, name='obtener_horas_disponibles'),

    # ==================== SISTEMA DE VETERINARIO ====================
    
    # Perfil y Configuración
    path('vet/perfil/', vet_perfil, name='vet_perfil'),
    
    # Gestión de Pacientes (Mascotas)
    path('vet/pacientes/', vet_pacientes, name='vet_pacientes'),
    path('vet/paciente/<int:paciente_id>/', vet_paciente_detalle, name='vet_paciente_detalle'),
    path('vet/paciente/crear/', vet_paciente_crear, name='vet_paciente_crear'),
    path('vet/paciente/crear/ajax/', vet_mascota_crear_ajax, name='vet_mascota_crear_ajax'),
    path('vet/paciente/<int:paciente_id>/editar/', vet_paciente_editar, name='vet_paciente_editar'),
    
    # Fichas Clínicas
    path('vet/fichas/', vet_fichas_clinicas, name='vet_fichas_clinicas'),
    path('vet/ficha/<int:ficha_id>/', vet_ficha_detalle, name='vet_ficha_detalle'),
    path('vet/ficha/crear/<int:paciente_id>/', vet_ficha_crear, name='vet_ficha_crear'),
    path('vet/ficha/<int:ficha_id>/editar/', vet_ficha_editar, name='vet_ficha_editar'),
    
    # Agenda y Citas
    path('vet/agenda/', vet_agenda, name='vet_agenda'),
    path('vet/agenda/api/', vet_agenda_api, name='vet_agenda_api'),
    path('vet/citas/', vet_citas, name='vet_citas'),
    path('vet/cita/<int:cita_id>/', vet_cita_detalle, name='vet_cita_detalle'),
    path('vet/cita/<int:cita_id>/eliminar/', vet_cita_eliminar, name='vet_cita_eliminar'),
    
    # Consultas Médicas
    path('vet/consultas/', vet_consultas, name='vet_consultas'),
    path('vet/consulta/<int:consulta_id>/', vet_consulta_detalle, name='vet_consulta_detalle'),
    path('vet/consulta/crear/', vet_consulta_crear_ajax, name='vet_consulta_crear_ajax'),
    path('vet/consulta/crear/old/', vet_consulta_crear, name='vet_consulta_crear'),
    path('vet/consulta/crear/<int:paciente_id>/', vet_consulta_crear, name='vet_consulta_crear_paciente'),
    path('vet/consulta/crear/cita/<int:cita_id>/', vet_consulta_crear, name='vet_consulta_crear_cita'),
    path('vet/consulta/<int:consulta_id>/editar/', vet_consulta_editar, name='vet_consulta_editar'),
    path('vet/consulta/<int:consulta_id>/completar/', vet_consulta_completar, name='vet_consulta_completar'),
    
    # Recetas y Prescripciones
    path('vet/recetas/', vet_recetas, name='vet_recetas'),
    path('vet/receta/<int:receta_id>/', vet_receta_detalle, name='vet_receta_detalle'),
    path('vet/receta/crear/<int:consulta_id>/', vet_receta_crear, name='vet_receta_crear'),
    path('vet/prescripcion/agregar/<int:receta_id>/', vet_prescripcion_agregar, name='vet_prescripcion_agregar'),
    
    # Vacunas
    path('vet/vacunas/', vet_vacunas, name='vet_vacunas'),
    path('vet/vacunas/<int:paciente_id>/', vet_vacunas, name='vet_vacunas_paciente'),
    path('vet/vacuna/registrar/<int:paciente_id>/', vet_vacuna_registrar, name='vet_vacuna_registrar'),
    
    # Tratamientos
    path('vet/tratamientos/', vet_tratamientos, name='vet_tratamientos'),
    path('vet/tratamientos/<int:paciente_id>/', vet_tratamientos, name='vet_tratamientos_paciente'),
    path('vet/tratamiento/registrar/<int:paciente_id>/', vet_tratamiento_registrar, name='vet_tratamiento_registrar'),
    
    # Inventario Médico
    path('vet/inventario/', vet_inventario, name='vet_inventario'),
    path('vet/inventario/alertas/', vet_inventario_alertas, name='vet_inventario_alertas'),
    path('vet/egreso/registrar/', vet_egreso_registrar, name='vet_egreso_registrar'),
]





