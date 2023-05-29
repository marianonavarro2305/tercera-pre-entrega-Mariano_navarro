from django.shortcuts import render, redirect
from .models import Usuario, Producto, Compra
import csv


def home(request):
    return render(request, 'home.html')

def redirect_login(request):
    return redirect('login')

def redirect_registro(request):
    return redirect('registro')

def registro(request):
    if request.method == 'POST':
        email = request.POST['email']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        password = request.POST['password']

        # Validar si el usuario ya existe en la base de datos
        if Usuario.objects.filter(email=email).exists():
            return redirect('registro')  # Redirigir a la página de registro nuevamente si el usuario ya existe

        # Crear un nuevo usuario en la base de datos
        usuario = Usuario(email=email, nombre=nombre, apellido=apellido, password=password)
        usuario.save()

        return redirect('login')  # Redirigir al usuario a la página de inicio de sesión después del registro

    return render(request, 'registro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Validar las credenciales del usuario en la base de datos
        if Usuario.objects.filter(email=email, password=password).exists():
            return redirect('inicio')  # Redirigir al usuario a la página de inicio después de iniciar sesión

    return render(request, 'login.html')


#def cargar_productos(request):
#    with open('productos.csv', 'r') as csv_file:
#        csv_reader = csv.reader(csv_file)
#        next(csv_reader)  # Omitir la primera fila si contiene encabezados
#
#        for row in csv_reader:
#            nombre = row[0]  # Columna del CSV que contiene el nombre del producto
#            precio = row[1]  # Columna del CSV que contiene el precio del producto
#
#            producto = Producto(nombre=nombre, precio=precio)
#            producto.save()
#
#    return HttpResponse('Datos de productos cargados correctamente.')
#
#
#def inicio(request):
#    productos = Producto.objects.all()
#    return render(request, 'inicio.html', {'productos': productos})

def inicio(request):
    # Verificar si ya existen productos en la base de datos
    if not Producto.objects.exists():
        
        with open('productos.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Omitir la primera fila si contiene encabezados

            for row in csv_reader:
                
                nombre = row[0]  # Columna del CSV que contiene el nombre del producto
                precio = row[1]  # Columna del CSV que contiene el precio del producto

                producto = Producto(nombre=nombre, precio=precio)
                producto.save()

    productos = Producto.objects.all()
    return render(request, 'inicio.html', {'productos': productos})


#def comprar(request):
#    if request.method == 'POST':
#        producto_id = request.POST['producto_ids']
#        cantidad = int(request.POST['cantidades'])
#
#        producto = Producto.objects.get(id=producto_id)
#        monto = producto.precio * cantidad
#
#        # Obtener el email del usuario logueado (si aplicara)
#        email = None
#        if request.user.is_authenticated:
#            email = request.user.email
#
#        # Guardar la compra en la tabla correspondiente
#        compra = Compra(producto=producto, cantidad=cantidad, monto=monto, email=email)
#        compra.save()
#
#        return redirect('confirmacion')
#
#    return redirect('inicio')
def comprar(request):
    if request.method == 'POST':
        producto_ids = request.POST.getlist('producto_ids[]')
        cantidades = request.POST.getlist('cantidades[]')

        for producto_id, cantidad in zip(producto_ids, cantidades):
            producto = Producto.objects.get(id=producto_id)
            cantidad = int(cantidad)

            monto = producto.precio * cantidad

            # Obtener el email del usuario logueado (si aplicara)
            email = None
            if request.user.is_authenticated:
                email = request.user.email

            # Guardar la compra en la tabla correspondiente
            compra = Compra(producto=producto, cantidad=cantidad, monto=monto, email=email)
            compra.save()

        return redirect('confirmacion')

    return redirect('inicio')


def confirmacion(request):
    # Obtener el email del usuario logueado (si aplicara)
    email = None
    if request.user.is_authenticated:
        email = request.user.email

    # Obtener la última compra realizada por el usuario
    ultima_compra = Compra.objects.filter(email=email).order_by('-id').first()

    return render(request, 'confirmacion.html', {'ultima_compra': ultima_compra})