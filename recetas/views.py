from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  #Para formularios, crear y autenticar 
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import PublisForm
from django.db import IntegrityError
from .models import Publicaciones
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from PIL import Image
from io import BytesIO
from django.core.files import File
from .forms import CalificacionForm
from .models import Publicaciones, Calificacion
from django.db.models import Avg
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserEditForm
from .forms import AvatarForm

from .models import Avatar

# Create your views here.

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{'form': UserCreationForm})#Variable form de UserCrationForm
        print('Enviando formulario')
    else:
        if request.POST['password1'] == request.POST['password2']:
            
            try:
                #Registrando al usuario, guardar solo en la base de datos...
                user = User.objects.create_user(username=request.POST['username'],password =request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('recetas')  #Te redirecciona a recetas
            
            except IntegrityError: 
                return render(request,'signup.html',{'form': UserCreationForm, 'error': 'El usuario ya existe.'})
            
        return render(request,'signup.html',{'form': UserCreationForm, 'error': 'No coinciden las contraseñas, hágalo nuevamente.'})

@login_required
def recetas(request):
    recetas_x = Publicaciones.objects.all()
    
    # Procesar la búsqueda
    query = request.GET.get("q")
    if query:
        recetas_x = recetas_x.filter(
            Q(title__icontains=query) | Q(ingredientes__icontains=query) | Q(preparacion__icontains=query)
        )
    
    return render(request, 'recetas.html', {'recetas': recetas_x, 'query': query})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request,'iniciar_sesion.html',{'form': AuthenticationForm})
    
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])

        if user is None:
            return render(request,'iniciar_sesion.html',{'form': AuthenticationForm, 'error': 'El nombre de usuario o contraseña son incorrectas, por favor ingrese nuevamente sus datos.'})

        else:
            login(request, user)
            return redirect('recetas')

@login_required
def create_publis(request):
    if request.method == 'GET':
        return render(request, 'create_publis.html', {'form': PublisForm})

    if request.method == 'POST':
        form = PublisForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_form = form.save(commit=False)
            nueva_form.autor = request.user

            if request.FILES.get('imagen_p'):
                # Redimensionar la imagen original
                img = Image.open(request.FILES['imagen_p'])
                img = img.resize((1200, 500), Image.BICUBIC)
                img_io = BytesIO()
                img.save(img_io, 'JPEG')

                # Convertir BytesIO a un archivo temporal
                img_temp = File(img_io)
                nueva_form.imagen_p.save('nombre_de_archivo.jpg', img_temp)

                # Crear una versión redimensionada
                img_redimensionada = img.resize((500, 300), Image.BICUBIC)
                img_redimensionada_io = BytesIO()
                img_redimensionada.save(img_redimensionada_io, 'JPEG')

                # Convertir BytesIO a un archivo temporal
                img_redimensionada_temp = File(img_redimensionada_io)
                nueva_form.imagen_redimensionada.save('nombre_de_archivo_redimensionado.jpg', img_redimensionada_temp)

            nueva_form.save()
            return redirect('recetas')
        else:
            return render(request, 'create_publis.html', {'form': PublisForm, 'error': 'Por favor ingresa datos válidos.'})
        

def recetas_detail(request, recetas_id):
    receta = get_object_or_404(Publicaciones, pk=recetas_id)

    # Calcular el puntaje promedio de las calificaciones
    promedio_puntaje = Calificacion.objects.filter(
        receta=receta).aggregate(promedio=Avg('calificacion'))
    puntaje_promedio = promedio_puntaje['promedio']
    form_calificar = CalificacionForm()
    return render(request, 'recetas_detail.html', {'recetas': receta, 'puntaje_promedio': puntaje_promedio, 'form': form_calificar})

@login_required
def actualizar_receta(request, recetas_id):
    recetas = get_object_or_404(Publicaciones, pk=recetas_id)

    if request.method == 'POST':
        form = PublisForm(request.POST, request.FILES, instance=recetas)
        if form.is_valid():
            recetas = form.save(commit=False)
            recetas.fecha_actualizada = timezone.now()

            if request.FILES.get('imagen_p'):
                # Redimensionar la imagen original
                img = Image.open(request.FILES['imagen_p'])
                img = img.resize((1200, 500), Image.BICUBIC)
                img_io = BytesIO()
                img.save(img_io, 'JPEG')

                # Convertir BytesIO a un archivo temporal
                img_temp = File(img_io)
                recetas.imagen_p.save('nombre_de_archivo.jpg', img_temp)

                # Crear una versión redimensionada
                img_redimensionada = img.resize((500, 300), Image.BICUBIC)
                img_redimensionada_io = BytesIO()
                img_redimensionada.save(img_redimensionada_io, 'JPEG')

                # Convertir BytesIO a un archivo temporal
                img_redimensionada_temp = File(img_redimensionada_io)
                recetas.imagen_redimensionada.save('nombre_de_archivo_redimensionado.jpg', img_redimensionada_temp)

            recetas.save()
            return redirect('recetas_detail', recetas_id=recetas_id)
    else:
        form = PublisForm(instance=recetas)

    return render(request, 'actualizar_receta.html', {'form': form, 'recetas': recetas})

@login_required
def delete_receta(request, recetas_id):
    recetas = get_object_or_404(Publicaciones, pk=recetas_id)
    
    if request.method == 'POST':
        # Elimina la receta de la base de datos
        recetas.delete()
        return redirect('recetas')
    

@login_required
def mis_recetas(request):


    # Obtén el usuario que ha iniciado sesión
    usuario_actual = request.user
    
    # Filtra las recetas que tienen el mismo ID de usuario
    recetas_x = Publicaciones.objects.filter(autor=usuario_actual)
    
    # Procesar la búsqueda
    query = request.GET.get("q")
    if query:
        recetas_x = recetas_x.filter(
            Q(title__icontains=query) | Q(ingredientes__icontains=query) | Q(preparacion__icontains=query)
        )
    
    return render(request, 'mis_recetas.html', {'recetas': recetas_x, 'query': query})


@login_required
def calificar_receta(request, recetas_id):
    receta = get_object_or_404(Publicaciones, pk=recetas_id)
    
    # Verificar si el usuario ya ha calificado la receta
    existing_calificacion = Calificacion.objects.filter(receta=receta, usuario=request.user).first()
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.cleaned_data['calificacion']
            if existing_calificacion:
                # Si ya calificó, actualiza la calificación existente
                existing_calificacion.calificacion = calificacion
                existing_calificacion.save()
            else:
                # Si no ha calificado, crea una nueva calificación
                Calificacion.objects.create(receta=receta, usuario=request.user, calificacion=calificacion)
            # Redirige al usuario nuevamente a la página de detalles de la receta
            return redirect('recetas_detail', recetas_id=receta.id)
        else:
            # En caso de que el formulario no sea válido, puedes tomar alguna acción, como mostrar un mensaje de error o simplemente redirigir al usuario.
            # Aquí, estoy redirigiendo al usuario nuevamente a la página de detalles.
            return redirect('recetas_detail', recetas_id=receta.id)
    
    return redirect('recetas_detail', recetas_id=receta.id)


@login_required
def editarPerfil(request):
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, instance=request.user)

        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.set_password(informacion['password1'])
            usuario.last_name = informacion['last_name']
            usuario.first_name = informacion['first_name']
            usuario.save()

            return redirect('login1')
    else:
        miFormulario = UserEditForm(instance=request.user)

    return render(request, 'editar_perfil.html', {"miFormulario": miFormulario, "usuario": usuario})

def agregar_avatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar_anterior = Avatar.objects.filter(user=request.user)
            if (len(avatar_anterior) > 0):
                avatar_anterior.delete()
            avatar_nuevo = Avatar(user=request.user, imagen=form.cleaned_data["imagen"])
            avatar_nuevo.save()
            return redirect('agregar_avatar')
    else:
        form = AvatarForm()
    return render(request, 'agregar_avatar.html', {"form": form})



