"""
URL configuration for inventarioVeterinariaPamela project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from gestorProductos.views import logout_view
from gestorUser.views import index, vetInicio, vet_veterinario, login_redirect
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView


def root_redirect(request):
    """Redirige a login si no está autenticado, o a la página correspondiente si lo está"""
    if request.user.is_authenticated:
        # Usuario autenticado, redirigir según su rol
        return login_redirect(request)
    else:
        # Usuario no autenticado, redirigir al login
        return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', index, name='admin_index'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('logout', logout_view, name='logout'),
    path('login_redirect/', login_redirect, name='login_redirect'),
    path('vet_inicio/', vetInicio, name='vet_inicio'),
    path('vet_veterinario/', vet_veterinario, name='vet_veterinario'),
    path('usuarios/', include("gestorUser.urls")),
    path('', root_redirect, name='root'),
    path('productos/', include("gestorProductos.urls")),
]

