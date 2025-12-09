from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import (
    CategoriaRegistroForm, ProductosRegistroForm, PCProductosForm, PAProductosForm,
    PSProductosForm, AProductosForm, AGAProductosForm, AGCProductosForm,
    SnackGProductosForm, SnackPProductosForm, AntiparasitarioForm,
    MedicamentoForm, ShampooForm, CamaForm, CollarForm, JugueteForm,
    DatatableProductosForm, DatatableProductosPCForm, DatatableProductosPAForm,
    DatatableProductosPSForm, DatatableProductosAForm, DatatableAGAForm,
    DatatableAGCForm, DatatableSnackGForm, DatatableSnackPForm,
    DatatableAntiparasitarioForm, DatatableMedicamentoForm, DatatableShampooForm,
    DatatableCollarForm, DatatableCamaForm, DatatableJugueteForm, CheckoutForm
)
from .models import (
    Productos, Categoria, Carrito, PCProductos, PAProductos, PSProductos,
    AProductos, AGAProductos, AGCProductos, SnackGProductos, SnackPProductos,
    Antiparasitario, Medicamento, Shampoo, Cama, Collar, Juguete
)
from gestorUser.forms import CitaMedicaForm
from gestorUser.models import CitaMedica

# Create your views here.

# ===========================
# VISTAS DE SESIÓN
# ===========================

@login_required
def vetInicio(request):
    productos = Productos.objects.all().order_by('-id')

    # Get user's citas and appointment form
    citas_usuario = []
    formulario_cita = CitaMedicaForm()
    if request.user.is_authenticated:
        citas_usuario = CitaMedica.objects.filter(user=request.user).order_by('fecha', 'hora')
        
    return render(request,'gestorProductos/vetInicio.html',{
        'productos': productos,
        'formulario_cita': formulario_cita,
        'citas_usuario': citas_usuario,
    })

def logout_view(request):
    logout(request)  # Cierra la sesión
    messages.success(request, 'Has cerrado sesión correctamente.')

    # Redirige al login
    return redirect('login')  # Redirige a la página de inicio de sesión

# ===========================
# VISTAS DE DATATABLE
# ===========================
def datatable(request):
    productos = Productos.objects.all()
    data = {'productos':productos}
    return render(request,'gestorProductos/datatable.html', data)

def datatable2(request):
    pcproductos = PCProductos.objects.all()
    data = {'pcproductos':pcproductos}
    return render(request,'gestorProductos/datatable2.html', data)

def datatable3(request):
    paproductos = PAProductos.objects.all()
    data = {'paproductos':paproductos}
    return render(request,'gestorProductos/datatable3.html', data)

def datatable4(request):
    psproductos = PSProductos.objects.all()
    data = {'psproductos':psproductos}
    return render(request,'gestorProductos/datatable4.html', data)



# ===========================
# VISTAS DE PRODUCTOS PERROS
# ===========================
def ProductosPAData(request):
    paproductos = PAProductos.objects.all()
    data = {'paproductos':paproductos}
    return render(request,'gestorProductos/PAProductos.html', data)

def ProductosPCData(request):
    pcproductos = PCProductos.objects.all()
    data = {'pcproductos':pcproductos}
    return render(request,'gestorProductos/PCProductos.html', data)

def ProductosPSData(request):
    psproductos = PSProductos.objects.all()
    data = {'psproductos':psproductos}
    return render(request,'gestorProductos/PSProductos.html', data)

def ProductosAData(request):
    aproductos = AProductos.objects.all()
    data = {'aproductos':aproductos}
    return render(request,'gestorProductos/AProductos.html', data)

# ===========================
# VISTAS DE SOBRE NOSOTROS
# ===========================
def sobreData(request):
    """
    Vista para manejar la página 'Sobre Nosotros'.
    """
    contexto = {
        'titulo': 'Sobre Nosotros',
        'descripcion': 'Somos una veterinaria dedicada al cuidado y bienestar de tus mascotas. Con más de 10 años de experiencia, ofrecemos servicios personalizados, productos de calidad y atención médica profesional para asegurar la felicidad y salud de tus compañeros peludos.',
        'equipo': [
            {'nombre': 'Dr. Juan Pérez', 'rol': 'Veterinario Principal', 'descripcion': 'Especialista en pequeñas especies con 15 años de experiencia.'},
            {'nombre': 'Ana López', 'rol': 'Asistente Veterinaria', 'descripcion': 'Apasionada por el cuidado animal y experta en nutrición de mascotas.'},
            {'nombre': 'Carlos Martínez', 'rol': 'Gerente', 'descripcion': 'Encargado de la atención al cliente y gestión del negocio.'},
        ],
        'mision': 'Proporcionar atención de calidad para mejorar la vida de las mascotas y sus dueños.',
        'vision': 'Ser la veterinaria líder en nuestra comunidad, reconocida por el compromiso y excelencia en el cuidado de los animales.',
        'valores': ['Compromiso', 'Excelencia', 'Pasión por los animales', 'Empatía', 'Innovación']
    }
    return render(request, 'gestorProductos/sobreNosotros.html', contexto)

# ===========================
# VISTAS DE ALIMENTO PERRO
# ===========================
def alimentoPerroAData(request):
    # Mostrar todos los productos sin límite
    paproductos = PAProductos.objects.all().order_by('-id')
    return render(request, 'gestorProductos/alimentoPAdulto.html', {'paproductos': paproductos})

def alimentoPerroCData(request):
    # Mostrar todos los productos sin límite
    pcproductos = PCProductos.objects.all().order_by('-id')
    return render(request, 'gestorProductos/alimentoPCachorro.html', {'pcproductos': pcproductos})

def alimentoPerroSData(request):
    # Mostrar todos los productos sin límite
    psproductos = PSProductos.objects.all().order_by('-id')
    return render(request, 'gestorProductos/alimentoPSenior.html', {'psproductos': psproductos})

def antipulgasData(request):
    aproductos = AProductos.objects.all().order_by('-id')
    return render(request, 'gestorProductos/antipulgas.html', {'aproductos': aproductos})

# ======================================
# VISTAS DE ELIMINAR Y EDITAR PRODUCTOS
# ======================================
def eliminarProducto(request, codigo):
    try:
        # Convertir codigo a string ya que en el modelo es CharField pero la URL puede venir como int
        codigo_str = str(codigo)
        producto = Productos.objects.get(codigo=codigo_str)
        # Aquí va el código para eliminar el producto
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Redirige a la lista de productos
    except Productos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable')  # Redirige a una página donde se pueda ver el error
    except Exception as e:
        messages.error(request, f"Error al eliminar el producto: {str(e)}")
        return redirect('datatable')


def editarProducto(request, id):
    # Busca el producto según el id
    producto = get_object_or_404(Productos, id=id)

    if request.method == 'POST':
        # Crea el formulario con datos enviados y la instancia del producto
        form = DatatableProductosForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Guarda los cambios en el modelo
            return redirect('datatable')  # Redirige a la lista de productos
    else:
        # Crea el formulario con la instancia del producto existente
        form = DatatableProductosForm(instance=producto)

    return render(request, 'gestorProductos/editarProducto.html', {'form': form, 'producto': producto})

# ============================================
# VISTAS DE ELIMINAR Y EDITAR PERRO CACHORRO
# ============================================
def eliminarProductoPC(request, codigo):
    try:
        pcproducto = PCProductos.objects.get(codigo=codigo)
        # Aquí va el código para eliminar el producto
        pcproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Redirige al catálogo de perros
    except PCProductos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable')  # Redirige al catálogo de perros



# ===========================================
# VISTAS DE ELIMINAR Y EDITAR PERRO ADULTO
# ===========================================
def eliminarProductoPA(request, codigo):
    try:
        paproducto = PAProductos.objects.get(codigo=codigo)
        paproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Ajusta con el nombre de tu vista de lista
    except PAProductos.DoesNotExist:
        messages.error(request, f"Producto con codigo {codigo} no encontrado.")
        return redirect('datatable')

# EDITAR PRODUCTO
def editarProductoPA(request, codigo):
    paproducto = get_object_or_404(PAProductos, codigo=codigo)

    if request.method == 'POST':
        form = DatatableProductosPAForm(request.POST, instance=paproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableProductosPAForm(instance=paproducto)

    return render(request, 'gestorProductos/editarProductoPA.html', {'form': form, 'paproducto': paproducto})

def editarProductoPC(request, codigo):
    # Busca el producto según el codigo
    pcproducto = get_object_or_404(PCProductos, codigo=codigo)

    if request.method == 'POST':
        # Crea el formulario con datos enviados y la instancia del producto
        form = DatatableProductosPCForm(request.POST, instance=pcproducto)
        if form.is_valid():
            form.save()  # Guarda los cambios en el modelo
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        # Crea el formulario con la instancia del producto existente
        form = DatatableProductosPCForm(instance=pcproducto)

    return render(request, 'gestorProductos/editarProductoPC.html', {'form': form, 'pcproducto': pcproducto})

def editarProductoPS(request, codigo):
    # Busca el producto según el codigo
    psproducto = get_object_or_404(PSProductos, codigo=codigo)

    if request.method == 'POST':
        # Crea el formulario con datos enviados y la instancia del producto
        form = DatatableProductosPSForm(request.POST, instance=psproducto)
        if form.is_valid():
            form.save()  # Guarda los cambios en el modelo
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        # Crea el formulario con la instancia del producto existente
        form = DatatableProductosPSForm(instance=psproducto)

    return render(request, 'gestorProductos/editarProductoPS.html', {'form': form, 'psproducto': psproducto})

# ==========================================
# VISTAS DE ELIMINAR Y EDITAR PERRO SENIOR
# ==========================================
def eliminarProductoPS(request, codigo):
    try:
        psproducto = PSProductos.objects.get(codigo=codigo)
        # Aquí va el código para eliminar el producto
        psproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Redirige al catálogo de perros
    except PSProductos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable')  # Redirige al catálogo de perros



# ========================================
# VISTAS DE ELIMINAR Y EDITAR ANTIPULGAS
# ========================================
def eliminarProductoA(request, codigo):
    try:
        aproducto = AProductos.objects.get(codigo=codigo)
        aproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Redirige al catálogo de perros
    except AProductos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable')  # Redirige al catálogo de perros

def editarProductoA(request, codigo):
    aproducto = get_object_or_404(AProductos, codigo=codigo)
    if request.method == 'POST':
        form = DatatableProductosAForm(request.POST, instance=aproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableProductosAForm(instance=aproducto)
    return render(request, 'gestorProductos/editarProductoA.html', {'form': form, 'aproducto': aproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR GATO ADULTO
# ========================================
def eliminarProductoAGA(request, codigo):
    try:
        agaproducto = AGAProductos.objects.get(codigo=codigo)
        agaproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable2')  # Redirige al catálogo de gatos
    except AGAProductos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable2')  # Redirige al catálogo de gatos

def editarProductoAGA(request, codigo):
    agaproducto = get_object_or_404(AGAProductos, codigo=codigo)
    if request.method == 'POST':
        form = DatatableAGAForm(request.POST, instance=agaproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableAGAForm(instance=agaproducto)
    return render(request, 'gestorProductos/editarProductoAGA.html', {'form': form, 'agaproducto': agaproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR GATO CACHORRO
# ========================================
def eliminarProductoAGC(request, codigo):
    try:
        agcproducto = AGCProductos.objects.get(codigo=codigo)
        agcproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable2')  # Redirige al catálogo de gatos
    except AGCProductos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable2')  # Redirige al catálogo de gatos

def editarProductoAGC(request, codigo):
    agcproducto = get_object_or_404(AGCProductos, codigo=codigo)
    if request.method == 'POST':
        form = DatatableAGCForm(request.POST, instance=agcproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableAGCForm(instance=agcproducto)
    return render(request, 'gestorProductos/editarProductoAGC.html', {'form': form, 'agcproducto': agcproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR SNACK GATO
# ========================================
def eliminarProductoSnackG(request, codigo):
    try:
        snackgproducto = SnackGProductos.objects.get(codigo=codigo)
        snackgproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable2')  # Redirige al catálogo de gatos
    except SnackGProductos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable2')  # Redirige al catálogo de gatos

def editarProductoSnackG(request, codigo):
    snackgproducto = get_object_or_404(SnackGProductos, codigo=codigo)
    if request.method == 'POST':
        form = DatatableSnackGForm(request.POST, instance=snackgproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableSnackGForm(instance=snackgproducto)
    return render(request, 'gestorProductos/editarProductoSnackG.html', {'form': form, 'snackgproducto': snackgproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR SNACK PERRO
# ========================================
def eliminarProductoSnackP(request, codigo):
    try:
        snackpproducto = SnackPProductos.objects.get(codigo=codigo)
        snackpproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Redirige al catálogo de perros
    except SnackPProductos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable')  # Redirige al catálogo de perros

def editarProductoSnackP(request, codigo):
    snackpproducto = get_object_or_404(SnackPProductos, codigo=codigo)
    if request.method == 'POST':
        form = DatatableSnackPForm(request.POST, instance=snackpproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableSnackPForm(instance=snackpproducto)
    return render(request, 'gestorProductos/editarProductoSnackP.html', {'form': form, 'snackpproducto': snackpproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR ANTIPARASITARIO
# ========================================
def eliminarProductoAntiparasitario(request, codigo):
    try:
        antiparasitario = Antiparasitario.objects.get(codigo=codigo)
        antiparasitario.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable3')  # Redirige al catálogo de medicamentos
    except Antiparasitario.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable3')  # Redirige al catálogo de medicamentos

def editarProductoAntiparasitario(request, codigo):
    antiparasitario = get_object_or_404(Antiparasitario, codigo=codigo)
    if request.method == 'POST':
        form = DatatableAntiparasitarioForm(request.POST, instance=antiparasitario)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable3')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableAntiparasitarioForm(instance=antiparasitario)
    return render(request, 'gestorProductos/editarProductoAntiparasitario.html', {'form': form, 'antiparasitario': antiparasitario})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR MEDICAMENTO
# ========================================
def eliminarProductoMedicamento(request, codigo):
    try:
        medicamento = Medicamento.objects.get(codigo=codigo)
        medicamento.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable3')  # Redirige al catálogo de medicamentos
    except Medicamento.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable3')  # Redirige al catálogo de medicamentos

def editarProductoMedicamento(request, codigo):
    medicamento = get_object_or_404(Medicamento, codigo=codigo)
    if request.method == 'POST':
        form = DatatableMedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable3')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableMedicamentoForm(instance=medicamento)
    return render(request, 'gestorProductos/editarProductoMedicamento.html', {'form': form, 'medicamento': medicamento})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR SHAMPOO
# ========================================
def eliminarProductoShampoo(request, codigo):
    try:
        shampoo = Shampoo.objects.get(codigo=codigo)
        shampoo.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable3')  # Redirige al catálogo de medicamentos
    except Shampoo.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable3')  # Redirige al catálogo de medicamentos

def editarProductoShampoo(request, codigo):
    shampoo = get_object_or_404(Shampoo, codigo=codigo)
    if request.method == 'POST':
        form = DatatableShampooForm(request.POST, instance=shampoo)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable3')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableShampooForm(instance=shampoo)
    return render(request, 'gestorProductos/editarProductoShampoo.html', {'form': form, 'shampoo': shampoo, 'is_creating': False})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR COLLAR
# ========================================
def eliminarProductoCollar(request, codigo):
    try:
        collar = Collar.objects.get(codigo=codigo)
        collar.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable4')  # Redirige al catálogo de accesorios
    except Collar.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable4')  # Redirige al catálogo de accesorios

def editarProductoCollar(request, codigo):
    collar = get_object_or_404(Collar, codigo=codigo)
    if request.method == 'POST':
        form = DatatableCollarForm(request.POST, instance=collar)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableCollarForm(instance=collar)
    return render(request, 'gestorProductos/editarProductoCollar.html', {'form': form, 'collar': collar})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR CAMA
# ========================================
def eliminarProductoCama(request, codigo):
    try:
        cama = Cama.objects.get(codigo=codigo)
        cama.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable4')  # Redirige al catálogo de accesorios
    except Cama.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable4')  # Redirige al catálogo de accesorios

def editarProductoCama(request, codigo):
    cama = get_object_or_404(Cama, codigo=codigo)
    if request.method == 'POST':
        form = DatatableCamaForm(request.POST, instance=cama)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableCamaForm(instance=cama)
    return render(request, 'gestorProductos/editarProductoCama.html', {'form': form, 'cama': cama})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR JUGUETE
# ========================================
def eliminarProductoJuguete(request, codigo):
    try:
        juguete = Juguete.objects.get(codigo=codigo)
        juguete.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable4')  # Redirige al catálogo de accesorios
    except Juguete.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable4')  # Redirige al catálogo de accesorios

def editarProductoJuguete(request, codigo):
    juguete = get_object_or_404(Juguete, codigo=codigo)
    if request.method == 'POST':
        form = DatatableJugueteForm(request.POST, instance=juguete)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableJugueteForm(instance=juguete)
    return render(request, 'gestorProductos/editarProductoJuguete.html', {'form': form, 'juguete': juguete})

# ========================================
# REGISTRAR LOS DATOS EN FORMULARIOS
# ========================================
def crear_alimentopa(request):
    form = PAProductosForm()
    if request.method == "POST":
        form = PAProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoPA.html', {'form': form})

def crear_alimentopc(request):
    form = PCProductosForm()
    if request.method == "POST":
        form = PCProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoPC.html', {'form': form})

def crear_alimentops(request):
    form = PSProductosForm()
    if request.method == "POST":
        form = PSProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoPS.html', {'form': form})

def crear_snackp(request):
    form = SnackPProductosForm()
    if request.method == "POST":
        form = SnackPProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearSnackPerro.html', {'form': form})

def crear_alimentoga(request):
    form = AGAProductosForm()
    if request.method == "POST":
        form = AGAProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearAlimentoGA.html', {'form': form})

def crear_alimentogc(request):
    form = AGCProductosForm()
    if request.method == "POST":
        form = AGCProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearAlimentoGC.html', {'form': form})

def crear_snackg(request):
    form = SnackGProductosForm()
    if request.method == "POST":
        form = SnackGProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearSnackGato.html', {'form': form})

def crear_antiparasitario(request):
    form = AntiparasitarioForm()
    if request.method == "POST":
        form = AntiparasitarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable3')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearAntiparasitario.html', {'form': form})

def crear_shampoo(request):
    if request.method == "POST":
        form = ShampooForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shampoo creado correctamente.", extra_tags='shampoo')
            return redirect('datatable3')
        else:
            # No redirigir si hay errores, mostrar en la misma página
            messages.error(request, "Error al crear el shampoo. Verifica los datos.", extra_tags='shampoo')
    else:
        form = ShampooForm()
    return render(request, 'gestorProductos/editarProductoShampoo.html', {'form': form, 'is_creating': True})

def crear_medicamentos(request):
    if request.method == "POST":
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicamento creado correctamente.", extra_tags='medicamento')
            return redirect('datatable3')
        else:
            # No redirigir si hay errores, mostrar en la misma página
            messages.error(request, "Error al crear el medicamento. Verifica los datos.", extra_tags='medicamento')
    else:
        form = MedicamentoForm()
    return render(request, 'gestorProductos/crearMedicamentos.html', {'form': form})

def crear_collares(request):
    form = CollarForm()
    if request.method == "POST":
        form = CollarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearCollares.html', {'form': form})

def crear_camas(request):
    form = CamaForm()
    if request.method == "POST":
        form = CamaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearCamas.html', {'form': form})

def crear_juguetes(request):
    form = JugueteForm()
    if request.method == "POST":
        form = JugueteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearJuguetes.html', {'form': form})

def ProductoPCRegistro(request):
    form = PCProductosForm()
    if request.method == "POST":
        form = PCProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoPC.html', {'form': form})

def ProductoPARegistro(request):
    form = PAProductosForm()
    if request.method == "POST":
        form = PAProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoPA.html', {'form': form})

def ProductoPSRegistro(request):
    form = PSProductosForm()
    if request.method == "POST":
        form = PSProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoPS.html', {'form': form})

def AProductoRegistro(request):
    form = AProductosForm()
    if request.method == "POST":
        form = AProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoA.html', {'form': form})

def SnackPerroRegistro(request):
    form = SnackPProductosForm()
    if request.method == "POST":
        form = SnackPProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable')  # Redirige al catálogo de perros
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearSnackPerro.html', {'form': form})

def AlimentoGARegistro(request):
    form = AGAProductosForm()
    if request.method == "POST":
        form = AGAProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2')  # Redirige al catálogo de gatos
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearAlimentoGA.html', {'form': form})

def AlimentoGCRegistro(request):
    form = AGCProductosForm()
    if request.method == "POST":
        form = AGCProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2')  # Redirige al catálogo de gatos
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearAlimentoGC.html', {'form': form})

def SnackGatoRegistro(request):
    form = SnackGProductosForm()
    if request.method == "POST":
        form = SnackGProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2')  # Redirige al catálogo de gatos
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearSnackGato.html', {'form': form})

def antiparasitarioRegistro(request):
    form = AntiparasitarioForm()
    if request.method == "POST":
        form = AntiparasitarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable3')  # Redirige al catálogo de medicamentos
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearAntiparasitario.html', {'form': form})

def shampooRegistro(request):
    # Usar la misma lógica que crear_shampoo para evitar duplicación
    return crear_shampoo(request)

def medicamentosRegistro(request):
    # Usar la misma lógica que crear_medicamentos para evitar duplicación
    return crear_medicamentos(request)

def camasRegistro(request):
    form = CamaForm()
    if request.method == "POST":
        form = CamaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable4')  # Redirige al catálogo de accesorios
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearCamas.html', {'form': form})

def collaresRegistro(request):
    form = CollarForm()
    if request.method == "POST":
        form = CollarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable4')  # Redirige al catálogo de accesorios
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearCollares.html', {'form': form})

def juguetesRegistro(request):
    form = JugueteForm()
    if request.method == "POST":
        form = JugueteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable4')  # Redirige al catálogo de accesorios
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearJuguetes.html', {'form': form})

# ========================================

# ========================================
def home(request):
    # Si el usuario no está autenticado, redirigir al login
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())
    
    categorias = Categoria.objects.all()

    # KPIs solo para superusuarios (admin)
    if request.user.is_superuser:
        # Total productos
        total_productos = (
            Productos.objects.count() +
            PCProductos.objects.count() +
            PAProductos.objects.count() +
            PSProductos.objects.count() +
            AProductos.objects.count() +
            AGAProductos.objects.count() +
            AGCProductos.objects.count() +
            SnackGProductos.objects.count() +
            SnackPProductos.objects.count() +
            Antiparasitario.objects.count() +
            Medicamento.objects.count() +
            Shampoo.objects.count() +
            Cama.objects.count() +
            Collar.objects.count() +
            Juguete.objects.count()
        )

        # Total stock
        total_stock = (
            sum(Productos.objects.values_list('stock', flat=True)) +
            sum(PCProductos.objects.values_list('stock', flat=True)) +
            sum(PAProductos.objects.values_list('stock', flat=True)) +
            sum(PSProductos.objects.values_list('stock', flat=True)) +
            sum(AProductos.objects.values_list('stock', flat=True)) +
            sum(AGAProductos.objects.values_list('stock', flat=True)) +
            sum(AGCProductos.objects.values_list('stock', flat=True)) +
            sum(SnackGProductos.objects.values_list('stock', flat=True)) +
            sum(SnackPProductos.objects.values_list('stock', flat=True)) +
            sum(Antiparasitario.objects.values_list('stock', flat=True)) +
            sum(Medicamento.objects.values_list('stock', flat=True)) +
            sum(Shampoo.objects.values_list('stock', flat=True)) +
            sum(Cama.objects.values_list('stock', flat=True)) +
            sum(Collar.objects.values_list('stock', flat=True)) +
            sum(Juguete.objects.values_list('stock', flat=True))
        )

        # Valor inventario (suma precio * stock)
        valor_inventario = (
            sum(p.precio * p.stock for p in Productos.objects.all()) +
            sum(p.precio * p.stock for p in PCProductos.objects.all()) +
            sum(p.precio * p.stock for p in PAProductos.objects.all()) +
            sum(p.precio * p.stock for p in PSProductos.objects.all()) +
            sum(p.precio * p.stock for p in AProductos.objects.all()) +
            sum(p.precio * p.stock for p in AGAProductos.objects.all()) +
            sum(p.precio * p.stock for p in AGCProductos.objects.all()) +
            sum(p.precio * p.stock for p in SnackGProductos.objects.all()) +
            sum(p.precio * p.stock for p in SnackPProductos.objects.all()) +
            sum(p.precio * p.stock for p in Antiparasitario.objects.all()) +
            sum(p.precio * p.stock for p in Medicamento.objects.all()) +
            sum(p.precio * p.stock for p in Shampoo.objects.all()) +
            sum(p.precio * p.stock for p in Cama.objects.all()) +
            sum(p.precio * p.stock for p in Collar.objects.all()) +
            sum(p.precio * p.stock for p in Juguete.objects.all())
        )

        # Datos para gráficos
        categorias_count = {
            'Alimentos_Perro': PAProductos.objects.count() + PCProductos.objects.count() + PSProductos.objects.count(),
            'Alimentos_Gato': AGAProductos.objects.count() + AGCProductos.objects.count(),
            'Snacks': SnackPProductos.objects.count() + SnackGProductos.objects.count(),
            'Medicamentos': Antiparasitario.objects.count() + Medicamento.objects.count(),
            'Accesorios': Shampoo.objects.count() + Cama.objects.count() + Collar.objects.count() + Juguete.objects.count(),
            'Otros': Productos.objects.count() + AProductos.objects.count()
        }

        # Productos recientes (últimos 5 agregados)
        productos_recientes = []
        categorias_map = {
            'PAProductos': 'Alimento Perro Adulto',
            'PCProductos': 'Alimento Perro Cachorro',
            'PSProductos': 'Alimento Perro Senior',
            'AGAProductos': 'Alimento Gato Adulto',
            'AGCProductos': 'Alimento Gato Cachorro',
            'SnackPProductos': 'Snack Perro',
            'SnackGProductos': 'Snack Gato',
            'Antiparasitario': 'Medicamento',
            'Medicamento': 'Medicamento',
            'Shampoo': 'Accesorio',
            'Cama': 'Accesorio',
            'Collar': 'Accesorio',
            'Juguete': 'Accesorio',
            'Productos': 'General',
            'AProductos': 'General'
        }
        
        # Mapeo de modelos a URLs de editar y eliminar
        # Formato: (nombre_modelo, (edit_url_name, edit_param_type, delete_url_name, delete_param_type))
        urls_map = {
            'Productos': ('editarProducto', 'id', 'eliminarProducto', 'codigo_int'),
            'PCProductos': ('editarProductoPC', 'codigo', 'eliminarProductoPC', 'codigo'),
            'PAProductos': ('editarProductoPA', 'codigo', 'eliminarProductoPA', 'codigo'),
            'PSProductos': ('editarProductoPS', 'codigo', 'eliminarProductoPS', 'codigo'),
            'AProductos': ('editarProductoA', 'codigo', 'eliminarProductoA', 'codigo'),
            'AGAProductos': ('editarProductoAGA', 'codigo', 'eliminarProductoAGA', 'codigo'),
            'AGCProductos': ('editarProductoAGC', 'codigo', 'eliminarProductoAGC', 'codigo'),
            'SnackPProductos': ('editarProductoSnackP', 'codigo', 'eliminarProductoSnackP', 'codigo'),
            'SnackGProductos': ('editarProductoSnackG', 'codigo', 'eliminarProductoSnackG', 'codigo'),
            'Antiparasitario': ('editarProductoAntiparasitario', 'codigo', 'eliminarProductoAntiparasitario', 'codigo'),
            'Medicamento': ('editarProductoMedicamento', 'codigo', 'eliminarProductoMedicamento', 'codigo'),
            'Shampoo': ('editarProductoShampoo', 'codigo', 'eliminarProductoShampoo', 'codigo'),
            'Cama': ('editarProductoCama', 'codigo', 'eliminarProductoCama', 'codigo'),
            'Collar': ('editarProductoCollar', 'codigo', 'eliminarProductoCollar', 'codigo'),
            'Juguete': ('editarProductoJuguete', 'codigo', 'eliminarProductoJuguete', 'codigo'),
        }
        
        from django.urls import reverse
        for model in [Productos, PCProductos, PAProductos, PSProductos, AProductos, AGAProductos, AGCProductos, SnackGProductos, SnackPProductos, Antiparasitario, Medicamento, Shampoo, Cama, Collar, Juguete]:
            model_name = model.__name__
            url_config = urls_map.get(model_name, (None, None, None, None))
            edit_url_name, edit_param, delete_url_name, delete_param = url_config
            
            for producto in model.objects.order_by('-id')[:5]:
                producto.categoria_nombre = categorias_map.get(model_name, 'Otros')
                # Agregar URLs de editar y eliminar
                if edit_url_name and delete_url_name:
                    try:
                        # Construir URL de editar
                        if edit_param == 'id':
                            producto.url_editar = reverse(edit_url_name, args=[producto.id])
                        elif edit_param == 'codigo' and hasattr(producto, 'codigo'):
                            producto.url_editar = reverse(edit_url_name, args=[producto.codigo])
                        else:
                            producto.url_editar = '#'
                        
                        # Construir URL de eliminar
                        if delete_param == 'codigo_int' and hasattr(producto, 'codigo'):
                            # Productos usa código como int en la URL pero el código puede ser string
                            try:
                                # Intentar convertir a int si es posible, si no usar el código tal cual
                                codigo_int = int(producto.codigo)
                                producto.url_eliminar = reverse(delete_url_name, args=[codigo_int])
                            except (ValueError, TypeError):
                                # Si no se puede convertir a int, usar el código como string (aunque la URL espera int)
                                # Esto puede causar un error 404, pero es mejor que no tener URL
                                try:
                                    producto.url_eliminar = reverse(delete_url_name, args=[producto.codigo])
                                except:
                                    producto.url_eliminar = '#'
                        elif delete_param == 'codigo' and hasattr(producto, 'codigo'):
                            producto.url_eliminar = reverse(delete_url_name, args=[producto.codigo])
                        else:
                            producto.url_eliminar = '#'
                    except Exception as e:
                        # Si hay algún error al construir las URLs, usar '#'
                        producto.url_editar = '#'
                        producto.url_eliminar = '#'
                else:
                    producto.url_editar = '#'
                    producto.url_eliminar = '#'
                
                productos_recientes.append(producto)

        productos_recientes = sorted(productos_recientes, key=lambda x: x.id, reverse=True)[:5]

        context = {
            'categorias': categorias,
            'total_productos': total_productos,
            'total_stock': total_stock,
            'valor_inventario': valor_inventario,
            'categorias_count': json.dumps(categorias_count),  # Convertir a JSON string
            'productos_recientes': productos_recientes
        }
    else:
        context = {'categorias': categorias}

    return render(request, 'index.html', context)

def guardar_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')

        # Guardar en la base de datos
        Productos.objects.create(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria
        )
        return redirect('datatable4')  # Redirige a la página de éxito

# =================================
# VISTAS DE ALIMENTO Y SNACK GATO
# =================================
def alimentoGatoAData(request):
    # Mostrar todos los productos sin límite
    agaproductos = AGAProductos.objects.all().order_by()
    return render(request, 'gestorProductos/alimentoGAdulto.html', {'agaproductos': agaproductos})

def alimentoGatoCData(request):
    # Mostrar todos los productos sin límite
    agcproductos = AGCProductos.objects.all().order_by()
    return render(request, 'gestorProductos/alimentoGCachorro.html', {'agcproductos': agcproductos})

def Snack_gato(request):
    snackgproductos = SnackGProductos.objects.all().order_by()
    return render(request, 'gestorProductos/snackGato.html', {'snackgproductos': snackgproductos})

# ===========================
# VISTAS DE SNACK PERRO
# ===========================

def Snack_Perro(request):
    snackpproductos = SnackPProductos.objects.all().order_by()
    return render(request, 'gestorProductos/snackPerro.html', {'snackpproductos': snackpproductos})

# ===========================
# VISTAS DE OTROS PRODUCTOS
# ===========================
def medicamentos(request):
    medicamento = Medicamento.objects.all().order_by()
    return render(request, 'gestorProductos/medicamentos.html', {'medicamento': medicamento})

def antiparasitarios(request):
    antiparasitario = Antiparasitario.objects.all().order_by()
    return render(request, 'gestorProductos/antiparasitario.html', {'antiparasitario': antiparasitario})


def shampoos(request):
    shampoo = Shampoo.objects.all().order_by()
    return render(request, 'gestorProductos/shampoo.html', {'shampoo': shampoo})

def camas(request):
    cama = Cama.objects.all().order_by()
    return render(request, 'gestorProductos/camas.html', {'cama': cama})

def collares(request):
    collar = Collar.objects.all().order_by()
    return render(request, 'gestorProductos/collares.html', {'collar': collar})

def juguetes(request):
    juguete = Juguete.objects.all().order_by()
    return render(request, 'gestorProductos/juguetes.html', {'juguete': juguete})

# ===========================
# VISTAS DEL CARRITO
# ===========================

# --- VER CARRITO ---
def ver_carrito(request):
    if request.GET.get("clear") == "1":
        if "carrito" in request.session:
            del request.session["carrito"]
            request.session.modified = True
            messages.success(request, "Carrito vaciado correctamente.")
        return redirect("ver_carrito")

    carrito = request.session.get("carrito", {})
    total = sum(item["subtotal"] for item in carrito.values())

    # Guardar la URL anterior si no viene del propio carrito
    url_anterior = request.META.get("HTTP_REFERER")

    if url_anterior and "carrito" not in url_anterior:
        request.session["ultima_url"] = url_anterior

    return render(request, "gestorProductos/verCarrito.html", {
        "carrito": carrito,
        "total": total,
        "volver": request.session.get("ultima_url", "/")
    })


# --- AGREGAR AL CARRITO ---

def agregar_carrito(request, tipo, producto_id):
    """
    Añade un producto al carrito guardado en session.
    URL: carrito/agregar/<str:tipo>/<int:producto_id>/
    Se espera un POST con campo 'cantidad'. Si no es POST, redirige atrás.
    """
    # Solo aceptar POST para añadir
    if request.method != "POST":
        # si fue GET, simplemente redirigimos a la página anterior
        referer = request.META.get("HTTP_REFERER") or '/'
        return redirect(referer)

    # Mapeo de tipos (ajusta claves si usas otras abreviaciones)
    modelos = {
        "pa": PAProductos,
        "pc": PCProductos,
        "ps": PSProductos,
        "a": AProductos,
        "p": Productos,
        "ap": Antiparasitario,
        "aga": AGAProductos,
        "agc": AGCProductos,
        "snackp": SnackPProductos,
        "snackg": SnackGProductos,
        "med": Medicamento,
        "shampoo": Shampoo,
        "cama": Cama,
        "collar": Collar,
        "juguete": Juguete,
    }

    modelo = modelos.get(tipo)
    if not modelo:
        messages.error(request, "Tipo de producto inválido.")
        # preferible volver a la página previa
        return redirect(request.META.get("HTTP_REFERER", "/"))

    producto = get_object_or_404(modelo, id=producto_id)

    # obtener cantidad del POST (validar)
    try:
        cantidad = int(request.POST.get("cantidad", 1))
        if cantidad < 1:
            cantidad = 1
    except (ValueError, TypeError):
        cantidad = 1

    # session cart
    carrito = request.session.get("carrito", {})

    # usar una key que incluya tipo para evitar colisiones entre modelos
    key = f"{tipo}_{producto.id}"

    precio_unit = float(producto.precio) if producto.precio is not None else 0.0

    if key not in carrito:
        carrito[key] = {
            "tipo": tipo,
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": precio_unit,
            "cantidad": cantidad,
            "subtotal": round(precio_unit * cantidad, 2),
            # opcional: agregar imagen url si quieres mostrarlo en carrito
            "imagen": getattr(producto, "imagen").url if getattr(producto, "imagen", None) else "",
        }
    else:
        # sumar cantidad
        carrito[key]["cantidad"] += cantidad
        carrito[key]["subtotal"] = round(carrito[key]["cantidad"] * carrito[key]["precio"], 2)

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, f"Se agregó {cantidad} x {producto.nombre} al carrito.")

    # Intentamos volver a la página anterior; si no existe, ir a inicio
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    return redirect("vet_inicio")

# --- ACTUALIZAR CANTIDADES ---
def actualizar_carrito(request):
    if request.method == "POST":
        carrito = request.session.get("carrito", {})

        for key in carrito.keys():
            nueva_cantidad = int(request.POST.get(f"cantidad_{key}", 1))
            carrito[key]["cantidad"] = nueva_cantidad
            carrito[key]["subtotal"] = nueva_cantidad * carrito[key]["precio"]

        request.session["carrito"] = carrito

    return redirect("ver_carrito")

# --- ELIMINAR PRODUCTO ---

def eliminar_carrito(request, tipo, producto_id):
    carrito = request.session.get("carrito", {})
    key = f"{tipo}_{producto_id}"

    if key in carrito:
        del carrito[key]
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, "Producto eliminado correctamente del carrito.")
    else:
        messages.error(request, "Producto no encontrado en el carrito.")

    return redirect("ver_carrito")


# ===========================
# CHECKOUT Y PROCESO DE COMPRA
# ===========================

@login_required
def procesar_checkout(request):
    """
    Procesa el formulario de checkout y simula el proceso de pago.
    En una implementación real, aquí se integraría con una pasarela de pago.
    """
    carrito = request.session.get("carrito", {})
    
    # Validar que el carrito no esté vacío
    if not carrito:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de continuar.")
        return redirect("ver_carrito")
    
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            # Obtener datos del formulario
            datos_cliente = form.cleaned_data
            
            # Calcular total
            total = sum(item["subtotal"] for item in carrito.values())
            
            # En una implementación real, aquí se procesaría el pago con la pasarela
            # Por ahora, simulamos un proceso exitoso
            
            # Guardar información de la compra en la sesión para la página de confirmación
            request.session["compra_datos"] = {
                "nombre_completo": datos_cliente["nombre_completo"],
                "email": datos_cliente["email"],
                "telefono": datos_cliente["telefono"],
                "direccion": datos_cliente["direccion"],
                "ciudad": datos_cliente["ciudad"],
                "codigo_postal": datos_cliente["codigo_postal"],
                "metodo_pago": datos_cliente["metodo_pago"],
                "total": float(total),
                "carrito": carrito.copy(),  # Copia del carrito
            }
            
            # Generar número de orden simulado
            import random
            import string
            numero_orden = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            request.session["compra_datos"]["numero_orden"] = numero_orden
            
            # Vaciar el carrito después de procesar
            del request.session["carrito"]
            request.session.modified = True
            
            messages.success(request, f"¡Compra procesada exitosamente! Número de orden: {numero_orden}")
            return redirect("confirmar_compra")
        else:
            # Si hay errores en el formulario, mostrar mensajes
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        # Si es GET, crear formulario con datos del usuario si está autenticado
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                "nombre_completo": f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                "email": request.user.email or "",
            }
        form = CheckoutForm(initial=initial_data)
    
    # Calcular total para mostrar en el template
    total = sum(item["subtotal"] for item in carrito.values())
    
    return render(request, "gestorProductos/checkout.html", {
        "form": form,
        "carrito": carrito,
        "total": total,
    })


@login_required
def confirmar_compra(request):
    """
    Muestra la página de confirmación de compra con los detalles de la orden.
    """
    compra_datos = request.session.get("compra_datos")
    
    if not compra_datos:
        messages.warning(request, "No se encontró información de compra. Redirigiendo al inicio.")
        return redirect("vet_inicio")
    
    # Pasar los datos a la plantilla
    context = {
        "numero_orden": compra_datos.get("numero_orden", "N/A"),
        "nombre_completo": compra_datos.get("nombre_completo", ""),
        "email": compra_datos.get("email", ""),
        "telefono": compra_datos.get("telefono", ""),
        "direccion": compra_datos.get("direccion", ""),
        "ciudad": compra_datos.get("ciudad", ""),
        "codigo_postal": compra_datos.get("codigo_postal", ""),
        "metodo_pago": compra_datos.get("metodo_pago", ""),
        "total": compra_datos.get("total", 0),
        "carrito": compra_datos.get("carrito", {}),
    }
    
    # Limpiar datos de la sesión después de mostrar (opcional)
    # del request.session["compra_datos"]
    
    return render(request, "gestorProductos/confirmar_compra.html", context)


# ===========================
# APIS
# ===========================
def api_perros_adulto(request):
    productos = PAProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_perros_cachorro(request):
    productos = PCProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_perros_senior(request):
    productos = PSProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_perros_snacks(request):
    productos = SnackPProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_gatos_adulto(request):
    productos = AGAProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_gatos_cachorro(request):
    productos = AGCProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_gatos_snacks(request):
    productos = SnackGProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_antiparasitario(request):
    productos = Antiparasitario.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_shampoo(request):
    productos = Shampoo.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_medicamento(request):
    productos = Medicamento.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_collares(request):
    productos = Collar.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_camas(request):
    productos = Cama.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_juguetes(request):
    productos = Juguete.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_aproductos(request):
    productos = AProductos.objects.filter()
    return JsonResponse({"data": list(productos.values())})

# Endpoint para agregar producto (POST) — usa csrftoken desde JS (recomendado)
@require_http_methods(["POST"])
def agregar_producto(request):
    # si usas fetch/ajax con csrftoken esto funcionará
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    precio = request.POST.get('precio')
    stock = request.POST.get('stock')
    categoria = request.POST.get('categoria')

    if not all([nombre, descripcion, precio, stock, categoria]):
        return HttpResponseBadRequest("Faltan campos")

    p = Productos.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        categoria=categoria
    )
    return JsonResponse({'ok': True, 'id': p.pk})








