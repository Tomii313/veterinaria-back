from django.db import models

# Create your models here.

class Veterinario(models.Model):
    dni = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_contratacion = models.DateField(auto_now_add=True)
    fecha_nacimiento = models.DateField()

    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Horario(models.Model):
    dias = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE)    

    def __str__(self):
        return f"{self.veterinario} {self.dias} {self.hora_inicio} {self.hora_fin}"