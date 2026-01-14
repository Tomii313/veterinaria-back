from django.db import models

# Create your models here.

class Duenio(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=15)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    """ direccion = models.CharField(max_length=100, blank=True, null=True) """

    def __str__(self):
        return f"{self.nombre} - {self.apellido}"
    