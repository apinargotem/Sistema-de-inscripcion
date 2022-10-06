"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from cgitb import handler
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import authenticate
from gestión_académica import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('index/',views.index,name="index"),
    path('<slug:slug_text>', views.detalles, name="detalles"),
    path('index/<slug:slug_text>', views.detalles, name="detalles"),
    path('cursos/',views.cursos,name="cursos"),
    path('cursos/<slug:slug_text>',views.detalles,name="detalles"),
    path('atencion/',views.atencion,name="atencion"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/',views.registro,name="registro"),
    path('agregar/<int:producto_id>/', views.agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', views.restar_producto, name="Sub"),
    path('limpiar/', views.limpiar_carrito, name="CLS"),
    path('carrito/',views.carrito,name="carrito"),
    path('sala/', views.sala),
    path('get-token/', views.generate_token),
    path('new-user/', views.new_user),
    path('get-another-user/', views.get_another_user),
    path('login/',views.login,name="login"),
    path('registro/',views.login,name="registro"),
    path('contac/',views.contac,name="contac"),
    path('consultar/',views.consultar,name="consultar"), 
    path('consultasinscripcion/',views.consultasinscripcion,name="consultasinscripcion"),
    path('pdf/generatePDFCursos/', views.generatePDFCursos, name='generatePDF'),
    path('pdf/generatePDFPagos/', views.generatePDFPagos, name='generatePDF'),
    path('pdf/generatePDFCategorias/', views.generatePDFCategorias, name='generatePDF'),
    path('pdf/generatePDFUsuarios/', views.generatePDFUsuarios, name='generatePDF'),
    path('pdf/generatePDFInscripciones/', views.generatePDFInscripciones, name='generatePDF'),
    path('pago/', views.pago, name= 'pago'),
    path('contenido/',views.contenido,name="contenido"),
    path('categoria/<slug:slug_cat>',views.cat,name="cat"),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
handler404='gestión_académica.views.handling_404'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


