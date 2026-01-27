from django.db import models

# Create your models here.
class Internacion(models.Model):

    nivel_urgencia = [
        ("EMERGENCIA", "Emergencia"),
        ("OBSERVACION", "Observacion"),
        ("CONTROL", "Control"),
    ]

    animal = models.ForeignKey('animales.Animal', on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_salida = models.DateField(null=True, blank=True)
    motivo = models.TextField()
    veterinario = models.ForeignKey('veterinarios.Veterinario', on_delete=models.CASCADE)
    observaciones = models.TextField()
    nivel_urgencia = models.CharField(max_length=100, choices=nivel_urgencia, null=True, blank=True)
    jaula = models.ForeignKey('Jaulas', on_delete=models.CASCADE)

    def __str__(self):
        return f"Internacion {self.animal} {self.fecha_ingreso}"

    class Meta:
        verbose_name = "Internacion"
        verbose_name_plural = "Internaciones"

    


class Jaulas(models.Model):
    numero = models.IntegerField()
    disponible = models.BooleanField(default=True)
    

    def __str__(self):
        if self.disponible:
            return f"Jaula {self.numero} Disponible"
        else:
            return f"Jaula {self.numero} Ocupada"

    class Meta:
        verbose_name = "Jaula"
        verbose_name_plural = "Jaulas"


class Observaciones(models.Model):
    internacion = models.ForeignKey(Internacion, on_delete=models.CASCADE, related_name="historial_observaciones")
    veterinario = models.ForeignKey('veterinarios.Veterinario', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    observacion = models.TextField()

    def __str__(self):
        return f"Observacion {self.internacion} {self.fecha}"