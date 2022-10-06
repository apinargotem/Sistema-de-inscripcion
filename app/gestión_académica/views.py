from base64 import decode
from itertools import product
from turtle import position
from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect,get_object_or_404
from django.contrib import messages
import json
from django.http import JsonResponse
from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
import random
import time
from .models import Room
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Categoria
from .models import Inscripcion
from .models import Curso
from usuario.models import User
from .Carrito import Carrito
from .models import Pago
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login as authlogin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from io import BytesIO 
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
import sys
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest


# Create your views here.
def handling_404(request,exception):
    return render(request,'404.html',{})
def index(request):
    cursosListados=Curso.objects.filter(Estado=True)

    return render(request,"index.html",{"cursos":cursosListados})
def login(request):
    return render(request,"login.html")
@login_required()
def cursos(request):
    data = {}
    data['categoria_slug'] = categoria_slug = request.GET.get('categoria_slug')
    data['categoria'] = categoria = Categoria.objects.filter(slug=categoria_slug).first()
    cursos_excluir = Inscripcion.objects.values_list('Curso_id', flat=True).filter(Usuario=request.user)
    cursosListados = Curso.objects.filter(Estado=True).exclude(Codigo__in=cursos_excluir)
    categoriaListados = Categoria.objects.all()

    if categoria is not None:
        cursosListados = cursosListados.filter(Categoria=categoria)
    data['cursos'] = cursosListados
    data['categorias'] = categoriaListados
    return render(request, "cursos.html", data)

def detalles(request,slug_text):
    cursosListados=Curso.objects.filter(slug=slug_text)
    context={'cursos':cursosListados}
    return render(request,"detalles.html",context)

   

def cat(request, slug_cat=None):
    categoria = None
    categorias = Categoria.objects.all()
    cursos = Curso.objects.filter(Estado=True)
    if slug_cat:
        categoria = get_object_or_404(Categoria, slug=slug_cat)
        cursos = Curso.objects.filter(Categoria=Categoria)
    context = {'categoria': categoria, 'categorias': categorias, 'cursos': cursos}
    return render(request, 'cat.html', context)
def consultar(request):
    busemp=request.GET["busemp"]
    cursosListados=Curso.objects.filter(Nombre__icontains=busemp)
    return render(request,"cursos.html",{"cursos":cursosListados})
def consultasinscripcion(request):
    return render(request,"consultasinscripcion.html")

def registro(request):
    data={
        'form':CustomUserCreationForm()
    }
    if request.method =='POST':
        formulario=CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user=authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            authlogin(request,user)
            messages.success(request,'Logueado con éxito') 
            return redirect (to="index")
        data["form"]=formulario

    return render(request, "registration/registro.html",data)

def contac(request):
    if request.method =='POST':
         subject=request.POST["asunto"]
         message=request.POST["mensaje"] + " " + request.POST["email"]
         email_from=settings.EMAIL_HOST_USER
         recipient_list=["napancontacto@gmail.com"]
         send_mail(subject, message, email_from, recipient_list, fail_silently=False)    
         messages.success(request,'Correo enviado con exito') 
         return redirect("index")
    else:
     return render(request,"contac.html")
  
def identidad(request):

    return render(request,"identidad.html")
@login_required
def carrito(request):
    return render(request,"carrito.html")

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Curso.objects.get(Codigo=producto_id)
    if carrito.agregar(producto):
        messages.success(request, f'Curso {producto} agregado con éxitosamente')
    else:
        messages.warning(request, f'Curso {producto}  ya se encuentra agregado al carrito ')
    return redirect("cursos")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Curso.objects.get(Codigo=producto_id)
    carrito.eliminar(producto)
    messages.success(request,'Curso eliminado con éxito') 
    return redirect("carrito")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Curso.objects.get(Codigo=producto_id)
    carrito.restar(producto)
    messages.success(request,'Curso eliminado con éxito') 
    return redirect("carrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    messages.success(request,'Carrito limpiado con éxito') 
    return redirect("cursos")
def atencion(request):
    roomListados=Room.objects.all()
    return render(request,"atencion.html")
def sala(request):
    return render(request, "sala.html")

@login_required
def contenido(request):   
    cursosListados=Inscripcion.objects.filter(Usuario=request.user)
    return render(request,"contenido.html",{"cursos":cursosListados})

def generate_token(request):
    appId = '062e413d01eb41e28d285bdce9852200'
    appCertificate = '3e696b569d37403e931c0a2f13e9b98b'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 232)
    expiration_time_seconds = 3600 * 12
    current_time_stamp = time.time()
    privilegeExpiredTs = current_time_stamp + expiration_time_seconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)

@csrf_exempt
def new_user(request):
    data = json.loads(request.body)
    member, created = Room.objects.get_or_create(
        username=data['username'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'username': data['username']}, safe=False)


def get_another_user(request):
    # getting the parameters with GET request
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    # quering the another user
    member = Room.objects.get(
        uid=uid,
        room_name=room_name,
    )
    # Return back the username
    username = member.username
    return JsonResponse({'username': member.username}, safe=False)


class PayPalClient:
    def __init__(self):
        self.client_id = "AV1-YL9xUXXR7o24Z_uzC7XF9iPDk3jMG0-8k0W91DCGS9IFw5DrU96Y3vjPrTqbPixIikUxm_pmDW34"
        self.client_secret = "EGZkfobz0F4-uSQHxiNoY4H-wZjlF1FJqSK1yZo5t7JZp4XC-4a8xt-2OD3ZAsNigHatvJZipw5e-Ez1"

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, int)

def pago(request):
    data = json.loads(request.body)
    order_id = data['orderID']

    detalle = GetOrder().get_order(order_id)
    detalle_precio = float(detalle.result.purchase_units[0].amount.value)
    carrito = Carrito(request)
    if detalle_precio:
        trx = CaptureOrder().capture_order(order_id, debug=True)
        pedido = Pago(
            id= trx.result.id, 
            estado= trx.result.status, 
            codigo_estado= trx.status_code, 
            total_de_la_compra = trx.result.purchase_units[0].payments.captures[0].amount.value, 
            nombre_cliente= trx.result.payer.name.given_name, 
            apellido_cliente= trx.result.payer.name.surname, 
            correo_cliente= trx.result.payer.email_address, 
            direccion_cliente= trx.result.purchase_units[0].shipping.address.address_line_1)
        pedido.save()
        for item in carrito.carrito:
           Inscripcion.objects.create(Pago=pedido,Curso_id=item['producto_id'],Usuario=request.user)
           carrito.limpiar()

        data = {
            "id": f"{trx.result.id}",
            "nombre_cliente": f"{trx.result.payer.name.given_name}",
            "status":True,
            "mensaje": "Pago realizado con éxito"
        }
        send_mail(
        'Inscripción de cursos',
        'Hola, hemos recibido tu pago con éxito, gracias por preferirnos, su usuario de moodle es el mismo que ya tiene registrado en nuestro sistema y su contraseña es: Gesti*  +  "su número de identidad", ejemplo Gesti*0123456789, también puede visualizarlo en la pestaña de consultas opción consulta de cursos y credenciales, caso contrario comuniquese a servicio al cliente',
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False)
        return JsonResponse(data)
    else:
        data = {
            "status":False,
            "mensaje": "Error, vuelva a intentar nuevamente"
             
        }
        return JsonResponse(data)

## Obtener los detalles de la transacción
class GetOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """You can use this function to retrieve an order by passing order ID as an argument"""   
  def get_order(self, order_id):
    """Method to get order"""
    request = OrdersGetRequest(order_id)
    #3. Call PayPal to get the transaction
    response = self.client.execute(request)
    return response
    #4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
    # print 'Status Code: ', response.status_code
    # print 'Status: ', response.result.status
    # print 'Order ID: ', response.result.id
    # print 'Intent: ', response.result.intent
    # print 'Links:'
    # for link in response.result.links:
    #   print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    # print 'Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
    #                    response.result.purchase_units[0].amount.value)

# """This driver function invokes the get_order function with
#    order ID to retrieve sample order details. """
# if __name__ == '__main__':
#   GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')


class CaptureOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, debug=False):
    """Method to capture order using order_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      print ('Order ID: ', response.result.id)
      print ('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print ('Capture Ids: ')
      for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
          print ('\t', capture.id)
      print ("Buyer:")
        # print "\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
        # response.result.payer.name.given_name + " " + response.result.payer.name.surname,
        # response.result.payer.phone.phone_number.national_number)
    return response

"""This driver function invokes the capture order function.
Replace Order ID value with the approved order ID. """
# if __name__ == "__main__":
#   order_id = 'REPLACE-WITH-APPORVED-ORDER-ID'
#   CaptureOrder().capture_order(order_id, debug=True)


##########PDF#########################


@staff_member_required
def generatePDFCursos(request):
    print ("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "cursos.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    cursos = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Cursos", styles['Heading1'])
    cursos.append(header)
    headings = ('Codigo', 'Nombre','Horas','Valor')
    allcursos= [(p.Codigo, p.Nombre, p.Horas, p.Valor) for p in Curso.objects.filter(Estado=True)]
    print(allcursos)

    t = Table([headings] + allcursos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    cursos.append(t)
    doc.build(cursos)
    response.write(buff.getvalue())
    buff.close()
    return response
  

def generatePDFPagos(request):
    print ("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "pagos.pdf"  # llamado clientes
    # la linea  es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    pagos = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Pagos", styles['Heading1'])
    pagos.append(header)
    headings = ('ID','Total de la compra','Nombre','Apellido','Correo','Fecha de pago')
    allpagos= [(p.id, p.total_de_la_compra, p.nombre_cliente, p.apellido_cliente, p.correo_cliente, p.fecha_pago) for p in Pago.objects.all()]
    print(allpagos)

    t = Table([headings] + allpagos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    pagos.append(t)
    doc.build(pagos)
    response.write(buff.getvalue())
    buff.close()
    return response

def generatePDFUsuarios(request):
    print ("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "usuarios.pdf"  # llamado clientes
    # la linea  es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    usuarios = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Usuarios", styles['Heading1'])
    usuarios.append(header)
    headings = ('Codigo','Usuario', 'Nombre', 'Apellido', 'Cedula', 'E-mail')
    allusuarios= [(p.id, p.username, p.first_name, p.last_name, p.cedula, p.email) for p in User.objects.filter(is_active=True)]
    print(allusuarios)

    t = Table([headings] + allusuarios)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    usuarios.append(t)
    doc.build(usuarios)
    response.write(buff.getvalue())
    buff.close()
    return response


def generatePDFCategorias(request):
    print ("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "categorias.pdf"  # llamado clientes
    # la linea  es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    categorias = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Categorias", styles['Heading1'])
    categorias.append(header)
    headings = ('Codigo', 'Nombre')
    allcategorias= [(p.Codigo, p.Nombre) for p in Categoria.objects.all()]
    print(allcategorias)

    t = Table([headings] + allcategorias)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    categorias.append(t)
    doc.build(categorias)
    response.write(buff.getvalue())
    buff.close()
    return response

def generatePDFInscripciones(request):
    print ("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "inscripciones.pdf"  # llamado clientes
    # la linea  es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    inscripciones = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de inscripciones", styles['Heading1'])
    inscripciones.append(header)
    headings = ('Usuario', 'Pago', 'Curso', 'Fecha de Inscripcion')
    allinscripciones= [(p.Usuario, p.Pago_id, p.Curso, p.FechaInscripcion) for p in Inscripcion.objects.all()]
    print(allinscripciones)

    t = Table([headings] + allinscripciones)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    inscripciones.append(t)
    doc.build(inscripciones)
    response.write(buff.getvalue())
    buff.close()
    return response

























    

