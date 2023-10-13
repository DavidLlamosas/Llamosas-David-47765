"""
URL configuration for Mi_Recetario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from recetas import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),         #Pestaña principal
    path('signup/',views.signup, name='signup'),
    path('recetas/',views.recetas, name='recetas'),
    path('logout/',views.cerrar_sesion, name='logout'),
    path('login1/',views.iniciar_sesion,name='login1'),

    path('recetas/create/',views.create_publis, name='create_publis'),
    path('recetas/<int:recetas_id>',views.recetas_detail, name='recetas_detail'),

    path('recetas/<int:recetas_id>/calificar/', views.calificar_receta, name='calificar_receta'),
    
    path('recetas/<int:recetas_id>/actualizar/', views.actualizar_receta, name='actualizar_receta'),
    path('recetas/<int:recetas_id>/delete/', views.delete_receta, name='delete_receta'),

    path('recetas/mis/',views.mis_recetas, name='mis_recetas'),

    path('editar_perfil/',views.editarPerfil,name='editar_perfil'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)