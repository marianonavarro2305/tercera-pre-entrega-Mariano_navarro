from django.db import models
"""
   Después de definir el modelo, ejecutar las migraciones para crear la tabla en la base de datos utilizando los comandos 
   python manage.py makemigrations 
   y 
   python manage.py migrate
   """

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    class Meta:
        app_label = 'ortopedia'


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    class Meta:
        app_label = 'ortopedia'

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(null=True, blank=True)
    class Meta:
        app_label = 'ortopedia'

    def __str__(self):
        return f'Compra de {self.producto} por {self.email}'
