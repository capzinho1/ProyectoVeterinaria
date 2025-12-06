"""
Comando para verificar y corregir el perfil de veterinario de un usuario.
Uso: python manage.py fix_veterinario veterinario1
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestorUser.models import VeterinarioProfile


class Command(BaseCommand):
    help = 'Verifica y corrige el perfil de veterinario de un usuario'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario a verificar/corregir')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'Usuario encontrado: {username}')
            
            # Verificar si tiene perfil de veterinario
            try:
                perfil = VeterinarioProfile.objects.get(user=user)
                self.stdout.write(f'Perfil de veterinario encontrado: es_veterinario = {perfil.es_veterinario}')
                
                if not perfil.es_veterinario:
                    perfil.es_veterinario = True
                    perfil.save()
                    self.stdout.write(self.style.SUCCESS(f'[OK] Perfil actualizado: ahora es_veterinario = True'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'[OK] El usuario ya es veterinario'))
                    
            except VeterinarioProfile.DoesNotExist:
                # Crear perfil de veterinario
                VeterinarioProfile.objects.create(user=user, es_veterinario=True)
                self.stdout.write(self.style.SUCCESS(f'[OK] Perfil de veterinario creado para {username}'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'✗ Usuario "{username}" no encontrado'))
            
