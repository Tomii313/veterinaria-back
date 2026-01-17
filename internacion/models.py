from django.db import models

# Create your models here.
class Internacion(models.Model):
    animal = models.ForeignKey('animales.Animal', on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_salida = models.DateField(null=True, blank=True)
    motivo = models.TextField()
    veterinario = models.ForeignKey('veterinarios.Veterinario', on_delete=models.CASCADE)
    observaciones = models.TextField()
    jaula = models.IntegerField()