# Proyecto Veterinaria Pamela

Sistema de gestión de inventario y citas médicas para veterinaria desarrollado en Django.

## Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

**Nota:** Este proyecto usa SQLite como base de datos, por lo que NO requiere XAMPP ni MySQL.

## Instalación

### 1. Crear y activar entorno virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar migraciones

```bash
python manage.py migrate
```

### 4. Crear superusuario (Opcional)

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear un usuario administrador.

## Ejecutar el Proyecto

```bash
python manage.py runserver
```

El servidor se iniciará en `http://127.0.0.1:8000/`

## Estructura del Proyecto

- `gestorProductos/`: Gestión de inventario de productos
- `gestorUser/`: Gestión de usuarios y citas médicas
- `templates/`: Plantillas HTML
- `static/`: Archivos estáticos (CSS, JS, imágenes)

## Usuarios y Roles

- **Superusuario/Staff**: Acceso al panel de administración (`/index`)
- **Veterinarios**: Acceso al sistema completo de veterinario (`/vet_inicio`)
- **Clientes**: Acceso a la vista de productos y carrito (`/vet_inicio`)

## Base de Datos

El proyecto soporta tanto SQLite (`db.sqlite3`) como MySQL/MariaDB. Para desarrollo, SQLite no requiere configuración adicional.

## Documentación Completa

Para información detallada sobre todas las funcionalidades del sistema, consulta:
- **[DOCUMENTACION_COMPLETA.md](DOCUMENTACION_COMPLETA.md)** - Documentación completa del sistema de veterinario y todas las funcionalidades nuevas

## Notas

- El proyecto está configurado para desarrollo (DEBUG=True)
- Para producción, cambiar DEBUG a False y configurar ALLOWED_HOSTS
- La SECRET_KEY debe ser cambiada en producción

