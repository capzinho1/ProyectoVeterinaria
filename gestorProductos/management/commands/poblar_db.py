"""
Comando de gestión para poblar la base de datos con datos iniciales.
Uso: python manage.py poblar_db
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestorProductos.models import (
    Productos, PCProductos, PAProductos, PSProductos, AProductos,
    AGAProductos, AGCProductos, SnackGProductos, SnackPProductos,
    Antiparasitario, Medicamento, Shampoo, Cama, Collar, Juguete
)
from gestorUser.models import VeterinarioProfile


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos iniciales de ejemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando población de base de datos...'))

        # Crear usuarios de ejemplo
        self.crear_usuarios()
        
        # Crear productos de ejemplo
        self.crear_productos()
        
        # Crear medicamentos y antiparasitarios
        self.crear_medicamentos()
        
        # Crear accesorios
        self.crear_accesorios()

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada exitosamente!'))

    def crear_usuarios(self):
        """Crea usuarios de ejemplo"""
        self.stdout.write('Creando usuarios...')
        
        # Superusuario admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@veterinaria.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('  [OK] Usuario admin creado'))
        else:
            self.stdout.write(self.style.WARNING('  [-] Usuario admin ya existe'))

        # Veterinario
        if not User.objects.filter(username='veterinario1').exists():
            vet = User.objects.create_user(
                username='veterinario1',
                email='vet1@veterinaria.com',
                password='vet123'
            )
            VeterinarioProfile.objects.create(user=vet, es_veterinario=True)
            self.stdout.write(self.style.SUCCESS('  [OK] Usuario veterinario1 creado'))
        else:
            # Si el usuario ya existe, asegurarse de que tenga el perfil de veterinario
            vet = User.objects.get(username='veterinario1')
            VeterinarioProfile.objects.update_or_create(
                user=vet, 
                defaults={'es_veterinario': True}
            )
            self.stdout.write(self.style.SUCCESS('  [OK] Usuario veterinario1 actualizado con perfil de veterinario'))

        # Cliente
        if not User.objects.filter(username='cliente1').exists():
            cliente = User.objects.create_user(
                username='cliente1',
                email='cliente1@veterinaria.com',
                password='cliente123'
            )
            self.stdout.write(self.style.SUCCESS('  [OK] Usuario cliente1 creado'))
        else:
            self.stdout.write(self.style.WARNING('  [-] Usuario cliente1 ya existe'))

    def crear_productos(self):
        """Crea productos de ejemplo"""
        self.stdout.write('Creando productos...')

        # Alimentos para perros adultos
        productos_pa = [
            {'codigo': 'PA001', 'nombre': 'Royal Canin Adult', 'marca': 'Royal Canin', 
             'precio': 25000, 'stock': 50, 'descripcion': 'Alimento premium para perros adultos'},
            {'codigo': 'PA002', 'nombre': 'Pro Plan Adult', 'marca': 'Purina', 
             'precio': 22000, 'stock': 40, 'descripcion': 'Alimento balanceado para perros adultos'},
            {'codigo': 'PA003', 'nombre': 'Eukanuba Adult', 'marca': 'Eukanuba', 
             'precio': 23000, 'stock': 35, 'descripcion': 'Nutrición completa para adultos'},
        ]
        for p in productos_pa:
            PAProductos.objects.get_or_create(codigo=p['codigo'], defaults=p)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(productos_pa)} productos PA creados'))

        # Alimentos para perros cachorros
        productos_pc = [
            {'codigo': 'PC001', 'nombre': 'Royal Canin Puppy', 'marca': 'Royal Canin', 
             'precio': 26000, 'stock': 45, 'descripcion': 'Alimento para cachorros'},
            {'codigo': 'PC002', 'nombre': 'Pro Plan Puppy', 'marca': 'Purina', 
             'precio': 24000, 'stock': 30, 'descripcion': 'Nutrición para cachorros'},
        ]
        for p in productos_pc:
            PCProductos.objects.get_or_create(codigo=p['codigo'], defaults=p)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(productos_pc)} productos PC creados'))

        # Alimentos para perros senior
        productos_ps = [
            {'codigo': 'PS001', 'nombre': 'Royal Canin Senior', 'marca': 'Royal Canin', 
             'precio': 25000, 'stock': 25, 'descripcion': 'Alimento para perros senior'},
        ]
        for p in productos_ps:
            PSProductos.objects.get_or_create(codigo=p['codigo'], defaults=p)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(productos_ps)} productos PS creados'))

        # Alimentos para gatos adultos
        productos_aga = [
            {'codigo': 'AGA001', 'nombre': 'Royal Canin Adult Cat', 'marca': 'Royal Canin', 
             'precio': 20000, 'stock': 40, 'descripcion': 'Alimento para gatos adultos'},
            {'codigo': 'AGA002', 'nombre': 'Pro Plan Cat', 'marca': 'Purina', 
             'precio': 18000, 'stock': 35, 'descripcion': 'Nutrición completa para gatos'},
        ]
        for p in productos_aga:
            AGAProductos.objects.get_or_create(codigo=p['codigo'], defaults=p)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(productos_aga)} productos AGA creados'))

        # Alimentos para gatos cachorros
        productos_agc = [
            {'codigo': 'AGC001', 'nombre': 'Royal Canin Kitten', 'marca': 'Royal Canin', 
             'precio': 21000, 'stock': 30, 'descripcion': 'Alimento para gatitos'},
        ]
        for p in productos_agc:
            AGCProductos.objects.get_or_create(codigo=p['codigo'], defaults=p)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(productos_agc)} productos AGC creados'))

        # Snacks para perros
        snacks_p = [
            {'codigo': 'SNP001', 'nombre': 'Snacks Dentales Perro', 'marca': 'Pedigree', 
             'precio': 5000, 'stock': 60, 'descripcion': 'Snacks para limpieza dental'},
            {'codigo': 'SNP002', 'nombre': 'Premios Training', 'marca': 'Royal Canin', 
             'precio': 4500, 'stock': 50, 'descripcion': 'Premios para entrenamiento'},
        ]
        for p in snacks_p:
            SnackPProductos.objects.get_or_create(codigo=p['codigo'], defaults=p)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(snacks_p)} snacks perro creados'))

        # Snacks para gatos
        snacks_g = [
            {'codigo': 'SNG001', 'nombre': 'Snacks Gato Premium', 'marca': 'Whiskas', 
             'precio': 4000, 'stock': 55, 'descripcion': 'Snacks deliciosos para gatos'},
        ]
        for p in snacks_g:
            SnackGProductos.objects.get_or_create(codigo=p['codigo'], defaults=p)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(snacks_g)} snacks gato creados'))

    def crear_medicamentos(self):
        """Crea medicamentos y antiparasitarios"""
        self.stdout.write('Creando medicamentos...')

        # Antiparasitarios
        antiparasitarios = [
            {'codigo': 'ANT001', 'nombre': 'Bravecto', 'descripcion': 'Antiparasitario de acción prolongada', 
             'precio': 35000, 'stock': 20, 'tipo': 'antiparasitario'},
            {'codigo': 'ANT002', 'nombre': 'Nexgard', 'descripcion': 'Antiparasitario mensual', 
             'precio': 28000, 'stock': 25, 'tipo': 'antiparasitario'},
            {'codigo': 'ANT003', 'nombre': 'Frontline', 'descripcion': 'Antiparasitario tópico', 
             'precio': 15000, 'stock': 30, 'tipo': 'antiparasitario'},
        ]
        for a in antiparasitarios:
            Antiparasitario.objects.get_or_create(codigo=a['codigo'], defaults=a)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(antiparasitarios)} antiparasitarios creados'))

        # Medicamentos
        medicamentos = [
            {'codigo': 'MED001', 'nombre': 'Vitamina D3', 'descripcion': 'Suplemento vitamínico', 
             'precio': 12000, 'stock': 40, 'tipo': 'vitamina'},
            {'codigo': 'MED002', 'nombre': 'Calcio Plus', 'descripcion': 'Suplemento de calcio', 
             'precio': 10000, 'stock': 35, 'tipo': 'vitamina'},
        ]
        for m in medicamentos:
            Medicamento.objects.get_or_create(codigo=m['codigo'], defaults=m)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(medicamentos)} medicamentos creados'))

    def crear_accesorios(self):
        """Crea accesorios (shampoos, camas, collares, juguetes)"""
        self.stdout.write('Creando accesorios...')

        # Shampoos
        shampoos = [
            {'codigo': 'SHM001', 'nombre': 'Shampoo Antipulgas', 'marca': 'Bayer', 
             'precio': 8000, 'stock': 25, 'descripcion': 'Shampoo para control de pulgas'},
            {'codigo': 'SHM002', 'nombre': 'Shampoo Hipoalergénico', 'marca': 'Vet', 
             'precio': 7500, 'stock': 20, 'descripcion': 'Shampoo para piel sensible'},
        ]
        for s in shampoos:
            Shampoo.objects.get_or_create(codigo=s['codigo'], defaults=s)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(shampoos)} shampoos creados'))

        # Camas
        camas = [
            {'codigo': 'CAM001', 'nombre': 'Cama Ortopédica Grande', 'marca': 'PetBed', 
             'precio': 35000, 'stock': 10, 'descripcion': 'Cama ortopédica para perros grandes', 
             'tamaño': 'Grande', 'material': 'Espuma'},
            {'codigo': 'CAM002', 'nombre': 'Cama Suave Mediana', 'marca': 'Comfort', 
             'precio': 20000, 'stock': 15, 'descripcion': 'Cama suave para perros medianos', 
             'tamaño': 'Mediana', 'material': 'Algodón'},
        ]
        for c in camas:
            Cama.objects.get_or_create(codigo=c['codigo'], defaults=c)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(camas)} camas creadas'))

        # Collares
        collares = [
            {'codigo': 'COL001', 'nombre': 'Collar Ajustable', 'marca': 'PetSafe', 
             'precio': 12000, 'stock': 30, 'descripcion': 'Collar ajustable con identificación', 
             'tamaño': 'Mediano', 'material': 'Nylon'},
            {'codigo': 'COL002', 'nombre': 'Collar Antipulgas', 'marca': 'Seresto', 
             'precio': 25000, 'stock': 20, 'descripcion': 'Collar con protección antipulgas', 
             'tamaño': 'Ajustable', 'material': 'Plástico'},
        ]
        for c in collares:
            Collar.objects.get_or_create(codigo=c['codigo'], defaults=c)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(collares)} collares creados'))

        # Juguetes
        juguetes = [
            {'codigo': 'JUG001', 'nombre': 'Pelota Interactiva', 'marca': 'Kong', 
             'precio': 15000, 'stock': 25, 'descripcion': 'Pelota para entretenimiento', 
             'tipo': 'Pelota'},
            {'codigo': 'JUG002', 'nombre': 'Hueso de Goma', 'marca': 'Nylabone', 
             'precio': 10000, 'stock': 30, 'descripcion': 'Hueso para masticar', 
             'tipo': 'Hueso'},
        ]
        for j in juguetes:
            Juguete.objects.get_or_create(codigo=j['codigo'], defaults=j)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(juguetes)} juguetes creados'))

