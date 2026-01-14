from django.db import models

# Create your models here.
class Animal(models.Model):
    raza = models.CharField(max_length=100, null=True, blank=True)
    peso = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    edad = models.IntegerField()
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    duenio = models.ForeignKey('duenios.Duenio', on_delete=models.CASCADE, related_name="mascotas")
    """ veterinario = models.ForeignKey('veterinarios.Veterinario', on_delete=models.CASCADE) """

    def __str__(self):
        return f"{self.nombre} - {self.especie}"

class Estado(models.Model):

    estados = [
        ("TRATAMIENTO", "En Tratamiento"),
        ("VACUNACION", "Vacunación Pendiente"),
    ]
    estado = models.CharField(max_length=100, choices=estados)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.estado} - {self.animal}"

        