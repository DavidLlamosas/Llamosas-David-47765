from django.contrib import admin
from .models import Publicaciones
# Register your models here.
from .models import Avatar

class PublisAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_creation", )



admin.site.register(Publicaciones, PublisAdmin)

admin.site.register(Avatar)