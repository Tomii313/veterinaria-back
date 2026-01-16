from django.db import models

# Create your models here.
class Animal(models.Model):

    estados = [
        ("TRATAMIENTO", "En Tratamiento"),
        ("VACUNACION", "Vacunación Pendiente"),
        ("INTERNACION", "Internacion"),
        ("DESPARASITACION", "Desparasitacion"),
    ]
    raza = models.CharField(max_length=100, null=True, blank=True)
    peso = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    edad = models.IntegerField(null=True, blank=True)
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=100, null=True, blank=True)
    especie = models.CharField(max_length=50, null=True, blank=True)
    duenio = models.ForeignKey('duenios.Duenio', on_delete=models.CASCADE, related_name="mascotas", null=True, blank=True)
    estado = models.CharField(max_length=100, choices=estados, blank=True, null=True)
    """ veterinario = models.ForeignKey('veterinarios.Veterinario', on_delete=models.CASCADE) """

    def __str__(self):
        return f"{self.nombre} - {self.especie} {self.edad} AÑOS"


        