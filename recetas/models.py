from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Publicaciones(models.Model):
    
    title = models.CharField(max_length=100)
    fecha_creation = models.DateTimeField(auto_now_add=True) #Añade automaticamente la fecha por defecto
    fecha_actualizada = models.DateTimeField(null=True)

    ingredientes = models.TextField(blank=True)
    preparacion = models.TextField(blank=True)

    #imagen_p = models.ImageField(upload_to='secun/images')

    email_p = models.EmailField()
    contacto_tel = models.IntegerField(default=000000000)

    autor = models.ForeignKey(User, on_delete=models.CASCADE)   #Si se borra el usuario, se borran sus recetas

    imagen_p = models.ImageField(upload_to='secun/images', default='default_image.jpg')  # Campo de imagen
    imagen_redimensionada = models.ImageField(upload_to='redimens/images', default='default_image.jpg')


    def __str__(self):
        return self.title + ' by ' + self.autor.username
    

class Calificacion(models.Model):
    receta = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    

class Personas(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
    
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)
    