#!/usr/bin/env python
from datetime import datetime, timedelta
import os
import sys
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


SITE_ROOT = YOUR_PATH = os.path.dirname(os.path.realpath(__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(YOUR_PATH))
SITE_ROOT = os.path.join(SITE_ROOT, '')
your_djangoproject_home = os.path.split(SITE_ROOT)[0]
sys.path.append(your_djangoproject_home)
import time
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()

from gestión_académica.models import Categoria, Curso
from app import moodle

parent_grupoid = 0

bgrupo = moodle.BuscarCategoriasid(2)
print(f'Se encontro categoria {bgrupo}')
if bgrupo:
    if 'id' in bgrupo[0]:
        parent_grupoid = bgrupo[0]['id']
print(bgrupo)
for categoria in Categoria.objects.all():
    print(categoria)
    if parent_grupoid > 0:
        bperiodo = moodle.BuscarCategorias(categoria.idnumber())

        parent_periodoid = None
        if bperiodo:
            if 'id' in bperiodo[0]:
                parent_periodoid = bperiodo[0]['id']
        else:
            bperiodo = moodle.CrearCategorias(categoria.__str__(), categoria.idnumber(), u"DESCRIPCION: %s"%categoria.Nombre, parent=parent_grupoid)
            parent_periodoid = bperiodo[0]['id']
        print('CREA CATEGORIA: %s' % categoria)

        cursos = Curso.objects.filter(Categoria=categoria)

        for curso in cursos:
            idnumber_curso=curso.idnumber()
            bcurso = moodle.BuscarCursos('idnumber', idnumber_curso)
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
                    cursoid = curso.idcursomoodle
            else:
                startdate=datetime.now().date()
                enddate=startdate+timedelta(5)

                startdate = int(time.mktime(startdate.timetuple()))
                enddate = int(time.mktime(enddate.timetuple()))

                bcurso = moodle.CrearCursosTarjeta(u'%s' % curso.Nombre,
                                                   u"NOM_CORTO%s"%curso.Codigo,
                                                   parent_periodoid,
                                                   idnumber_curso,
                                                   curso.Descripcion,
                                                   startdate, enddate,
                                                   5)
                print(bcurso)
                cursoid = bcurso[0]['id']
            print('********Curso: %s' % curso)

            if cursoid > 0:
                if curso.Id_moodle != cursoid:
                    curso.Id_moodle= cursoid
                    curso.save()

                try:
                    curso.actualizar_estudiantes_curso(moodle)
                except Exception as ex:
                    print('Error al crear estudiante %s' % ex)