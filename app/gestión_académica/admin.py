from ast import And, Pass
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from gestión_académica.models import Categoria
from gestión_académica.models import Curso
from gestión_académica.models import Inscripcion
from gestión_académica.models import Room
from gestión_académica.models import Pago

class CategoriaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('Codigo','Nombre')
    list_display = ('Codigo','Nombre')
    change_list_template = 'admin/gestión_académica/Categoria/change_list.html'


pass


class CursoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  
  search_fields=('Codigo','Nombre','Horas','Valor','Descripcion')
  list_display = (
      'Codigo',
      'Nombre',
      'Horas',
      'Valor',
      'image_tag',
      'Descripcion',
      'Estado',
    ) 
  change_list_template = 'admin/gestión_académica/Curso/change_list.html'
pass
  
class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    raw_id_fields = ['Curso']

   


class InscripcionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields=['Usuario','Pago__nombre_cliente','Pago__apellido_cliente','Curso__Nombre']
    list_filter=['Usuario','Pago__nombre_cliente','Pago__apellido_cliente','Curso__Nombre','FechaInscripcion']
    list_display=('Usuario','Pago_id','Curso','FechaInscripcion')
    change_list_template = 'admin/gestión_académica/Inscripcion/change_list.html'


class RoomAdmin(ImportExportModelAdmin):
    search_fields=('username','uid','room_name')
    list_display = (
      'username',
      'uid',
      'room_name')

class PagoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  
  search_fields=('id','estado','codigo_estado','total_de_la_compra','nombre_cliente','apellido_cliente','correo_cliente','direccion_cliente','fecha_pago')
  list_display = (
      'id','estado','codigo_estado','total_de_la_compra','nombre_cliente','apellido_cliente','correo_cliente','direccion_cliente','fecha_pago'
    ) 
  inlines = [InscripcionInline]
  change_list_template = 'admin/gestión_académica/Pago/change_list.html'
pass



# Register your models here.

admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Curso,CursoAdmin)
admin.site.register(Room)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Inscripcion,InscripcionAdmin)
admin.site.site_header="Sistema de Inscripción"

