from django.db import models
import os
from datetime import datetime, timedelta
import time
from app import moodle
from usuario.models import User
from  django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.validators import MaxValueValidator
from decimal import Decimal
from django.db import models, connection, connections

class Categoria(models.Model):
    Codigo = models.CharField(max_length=20, primary_key=True)
    Nombre = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200, unique=True,blank=True)
    #Id_moodle = models.IntegerField()

    def __str__(self):
        txt = "{0}"
        return txt.format(self.Nombre)

    def idnumber(self):
        return u"CAT_%s"%(self.Codigo)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Nombre)
        super(Categoria, self).save(*args, **kwargs)
        parent_grupoid = 0
        bgrupo = moodle.BuscarCategoriasid(2)
        if bgrupo:
            if 'id' in bgrupo[0]:
                parent_grupoid = bgrupo[0]['id']
        print(bgrupo)
        if parent_grupoid > 0:
            bperiodo = moodle.BuscarCategorias(self.idnumber())
            if bperiodo:
                if 'id' in bperiodo[0]:
                    parent_periodoid = bperiodo[0]['id']
            else:
                bperiodo = moodle.CrearCategorias(self.__str__(), self.idnumber(),
                                                  u"DESCRIPCION: %s" % self.Nombre, parent=parent_grupoid)
                parent_periodoid = bperiodo[0]['id']
            print('CREA CATEGORIA: %s' % parent_periodoid)


    def get_absolute_url(self):
        return reverse('cursos', args=[self.slug])

    class Meta:
        verbose_name=u'Categoria'
        verbose_name_plural=u'Categorias'


class Curso(models.Model):
    Codigo = models.CharField(max_length=20, primary_key=True)
    Nombre = models.CharField(max_length=100, verbose_name="Curso")
    slug = models.SlugField(max_length=200, unique=True,blank=True)
    Categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    Horas= models.PositiveSmallIntegerField()
    Valor= models.FloatField()
    Imagen=models.ImageField(upload_to="cursos",null=True)
    Descripcion=models.TextField(max_length=10000)
    Fecha_Inicio= models.DateTimeField()
    Estado=models.BooleanField(default=True)
    Id_moodle=models.IntegerField(blank=True, null=True)

    def idnumber(self):
        return u"CUR_%s"%(self.Codigo)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.Nombre)
        super(Curso, self).save(*args, **kwargs)
        idnumber_curso = self.idnumber()
        bperiodo = moodle.BuscarCategorias(self.Categoria.idnumber())
        bcurso = moodle.BuscarCursos('idnumber', idnumber_curso)
        parent_periodoid = bperiodo[0]['id']
        if not bcurso:
            bcurso = moodle.BuscarCursos('idnumber', idnumber_curso)
        cursoid = 0
        # print(bcurso)
        if bcurso['courses']:
            # print(bcurso['courses'][0])
            if 'id' in bcurso['courses'][0]:
                cursoid = bcurso['courses'][0]['id']
                # print(cursoid)
            else:
                cursoid = self.idnumber()
        else:
            startdate = datetime.now().date()
            enddate = startdate + timedelta(5)

            startdate = int(time.mktime(startdate.timetuple()))
            enddate = int(time.mktime(enddate.timetuple()))

            bcurso = moodle.CrearCursosTarjeta(u'%s' % self.Nombre,
                                               u"NOM_CORTO%s" % self.Codigo,
                                               parent_periodoid,
                                               idnumber_curso,
                                               self.Descripcion,
                                               startdate, enddate,
                                               5)
            print(bcurso)
            cursoid = bcurso[0]['id']
        print('********Curso: %s' % bcurso[0]['id'])

        if cursoid > 0:
            if self.Id_moodle != cursoid:
                self.Id_moodle = cursoid
                models.Model.save(self)
            try:
                self.actualizar_estudiantes_curso(moodle)
            except Exception as ex:
                print('Error al crear estudiante %s' % ex)


    def actualizar_estudiantes_curso(self, moodle):
        cursor = connections['moodle'].cursor()
        if self.Id_moodle:
            contador = 0
            cursoid = self.Id_moodle
            rolestudiante = 5
            for inscripcion in Inscripcion.objects.filter(Curso=self):
                try:
                    contador += 1
                    estudianteid=0
                    busuario=None
                    usuario = inscripcion.Usuario
                    rolest=None
                    print("Verificando si esta enrolado: %s" % inscripcion)

                    queryest = """ SELECT DISTINCT asi.userid
                                FROM  mdl_role_assignments asi
                                INNER JOIN MDL_CONTEXT CON ON asi.CONTEXTID=CON.ID 
                                AND ASI.ROLEID=%s AND CON.INSTANCEID=%s AND asi.userid =%s
                                  """ % (rolestudiante, cursoid, inscripcion.Id_moodle)
                    cursor.execute(queryest)
                    rowest = cursor.fetchall()
                    if not rowest:
                        print("No esta matriculado, procediendo a enrolar: %s" % inscripcion)
                        username = usuario.username
                        busuario = moodle.BuscarUsuario('username', username)

                        if busuario['users']:
                            if 'id' in busuario['users'][0]:
                                estudianteid = busuario['users'][0]['id']
                        else:
                            idnumber_user = inscripcion.Usuario.cedula
                            bestudiante = moodle.CrearUsuario(u'%s' % inscripcion.Usuario.username,
                                                              u'%s' % inscripcion.Usuario.cedula,
                                                              u'%s' % inscripcion.Usuario.first_name,
                                                              u'%s' % inscripcion.Usuario.last_name,
                                                              u'%s' % inscripcion.Usuario.email,
                                                              idnumber_user,
                                                              u'GUAYAQUIL',
                                                              u'ECUADOR')
                            estudianteid = bestudiante[0]['id']
                        if estudianteid > 0:
                            rolest = moodle.EnrolarCurso(rolestudiante, estudianteid, cursoid)
                            if inscripcion.Id_moodle != estudianteid:
                                inscripcion.Id_moodle = estudianteid
                                inscripcion.save()
                        contador+=1
                        print('************Estudiante: %s *** %s idm: %s rol: %s est: %s' % ( contador, inscripcion, self.Id_moodle, rolest, estudianteid))
                except Exception as ex:
                    print('Error al crear estudiante %s' % ex)

    def delete(self,*args,**kwargs):
            if os.path.isfile(self.Imagen.path):
                os.remove(self.Imagen.path)
            super(Curso,self).delete(*args,**kwargs)

    def image_tag(self):
        from django.utils.html import escape, mark_safe
        url = '/static/imagenes/unip.png'
        if self.Imagen.name:
            url = self.Imagen.url
        return mark_safe(u'<img src="%s" width="100"  height="100"/>' % (url))



    image_tag.short_description = 'Imagen'
    image_tag.allow_tags = True


    def __str__(self):
        txt = "{0}"
        return txt.format(self.Nombre)

    
class Pago(models.Model):
    id = models.CharField(primary_key= True, max_length=100)
    estado = models.CharField(max_length=100)
    codigo_estado = models.CharField(max_length=100)
    total_de_la_compra = models.DecimalField(max_digits=5 ,decimal_places= 2)
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    correo_cliente = models.EmailField(max_length=100)
    direccion_cliente = models.CharField(max_length=100)
    fecha_pago= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre_cliente

class Inscripcion(models.Model):
    Pago =models.ForeignKey(Pago,related_name='items', on_delete=models.CASCADE)
    Curso= models.ForeignKey(Curso,related_name='order_items',on_delete=models.CASCADE)
    Usuario=models.ForeignKey(to=User,on_delete=models.CASCADE)
    FechaInscripcion = models.DateTimeField(auto_now_add=True)
    Id_moodle = models.IntegerField(default=0,blank=True, null=True)


    def __str__(self):
        return str(self.Usuario)
    class Meta:
        verbose_name_plural= "Inscripciones"
        verbose_name="Inscripción"

    def save(self, *args, **kwargs):
        super(Inscripcion, self).save(*args, **kwargs)
        cursor = connections['moodle'].cursor()
        if self.Curso.Id_moodle:
            cursoid = self.Curso.Id_moodle
            rolestudiante = 5
            try:
                estudianteid = 0
                busuario = None
                usuario = self.Usuario
                rolest = None
                print("Verificando si esta enrolado: %s" % self)
                queryest = """ SELECT DISTINCT asi.userid
                                FROM  mdl_role_assignments asi
                                INNER JOIN MDL_CONTEXT CON ON asi.CONTEXTID=CON.ID 
                                AND ASI.ROLEID=%s AND CON.INSTANCEID=%s AND asi.userid =%s
                                  """ % (rolestudiante, cursoid, self.Id_moodle)
                cursor.execute(queryest)
                rowest = cursor.fetchall()
                if not rowest:
                    print("No esta matriculado, procediendo a enrolar: %s" % self)
                    username = usuario.username
                    busuario = moodle.BuscarUsuario('username', username)
                    if busuario['users']:
                        if 'id' in busuario['users'][0]:
                            estudianteid = busuario['users'][0]['id']
                    else:
                        idnumber_user = self.Usuario.cedula
                        bestudiante = moodle.CrearUsuario(u'%s' % self.Usuario.username,
                                                          u'%s' % self.Usuario.cedula,
                                                          u'%s' % self.Usuario.first_name,
                                                          u'%s' % self.Usuario.last_name,
                                                          u'%s' % self.Usuario.email,
                                                          idnumber_user,
                                                          u'GUAYAQUIL',
                                                          u'ECUADOR')
                        estudianteid = bestudiante[0]['id']
                    if estudianteid > 0:
                        rolest = moodle.EnrolarCurso(rolestudiante, estudianteid, cursoid)
                        if self.Id_moodle != estudianteid:
                            self.Id_moodle = estudianteid
                            models.Model.save(self)
                    print('************Estudiante: %s idm: %s rol: %s est: %s' % ( self, self.Id_moodle, rolest, estudianteid))
            except Exception as ex:
                print(ex.__str__())
                pass

class Room(models.Model):
    username = models.CharField(max_length=10,verbose_name="nombre del usuario")
    uid = models.CharField(max_length=500)
    room_name = models.CharField(max_length=150, verbose_name="nombre de la sala")

    def __str__(self):
        return self.username
    def __unicode__(self):
        return self.room_name,self.username





