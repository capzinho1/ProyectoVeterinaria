from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# -------------------------------
# PRODUCTOS PERROS (GENERALES)
# -------------------------------

class Productos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PCProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PAProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class PSProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class AProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# -------------------------------
# CATEGORIA GENERAL
# -------------------------------

class Categoria(models.Model):
    mascota = models.CharField(max_length=200)
    producto = models.CharField(max_length=200)
    tipo_cuidado = models.CharField(max_length=200)
    tipo_alimento = models.CharField(max_length=200)
    accesorios = models.CharField(max_length=200)
    medicamentos = models.CharField(max_length=200)
    servicios_asociados = models.CharField(max_length=200)

    def __str__(self):
        return self.mascota


# -------------------------------
# ALIMENTOS GATO
# -------------------------------

class AGAProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class AGCProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# -------------------------------
# SNACKS
# -------------------------------

class SnackGProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class SnackPProductos(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# -------------------------------
# MEDICAMENTOS
# -------------------------------

class Antiparasitario(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('antiparasitario', 'Antiparasitario'),
            ('otros', 'Otros')
        ],
        default='otros'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
# -------------------------------
# MEDICAMENTOS
# -------------------------------

class Medicamento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('vitamina', 'Vitamina'),
            ('otros', 'Otros')
        ],
        default='otros'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


# -------------------------------
# SHAMPOOS
# -------------------------------

class Shampoo(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# -------------------------------
# CAMAS
# -------------------------------

class Cama(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre
    

# -------------------------------
# COLLARES
# -------------------------------

class Collar(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre


# -------------------------------
# JUGUETES
# -------------------------------

class Juguete(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
# -------------------------------
# CARRITO
# -------------------------------

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carrito')
    producto_tipo = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    producto_id = models.PositiveIntegerField()
    producto = GenericForeignKey('producto_tipo', 'producto_id')
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto} x {self.cantidad}"


# -------------------------------
# IMÁGENES DE PRODUCTOS
# -------------------------------

class ImagenProducto(models.Model):
    """
    Modelo para almacenar múltiples imágenes de productos usando GenericForeignKey.
    Permite relacionar imágenes con cualquier tipo de producto.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    
    url_imagen = models.URLField(max_length=500, verbose_name="URL de la imagen")
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización (0 = primera)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['orden', 'fecha_creacion']
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"
    
    def __str__(self):
        return f"Imagen de {self.producto} (Orden: {self.orden})"