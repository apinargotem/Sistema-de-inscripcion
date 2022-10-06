from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from usuario.models import User


# Register your models here.
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['username', 'first_name', 'last_name__icontains' , 'email', 'cedula']
    #list_filter=['username','Pago__nombre_cliente','Pago__apellido_cliente','Curso__Nombre']
    list_display = ('username', 'first_name', 'last_name', 'cedula', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    change_list_template = 'admin/usuario/User/change_list.html'
pass

admin.site.register(User, UserAdmin)