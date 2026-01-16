from django.db import models

# Create your models here.

estados = [
    ("Pendiente", "Pendiente"),
    ("Confirmado", "Confirmado"),
    ("Cancelado", "Cancelado"),
    ("Reprogramado", "Reprogramado"),
    ("Finalizado", "Finalizado"),
]


class Turno(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=100)
    animal = models.ForeignKey('animales.Animal', on_delete=models.CASCADE, null=True, blank=True)
    veterinario = models.ForeignKey('veterinarios.Veterinario', on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=estados, default="Pendiente")


    class Meta:
        unique_together = ('veterinario', 'fecha', 'hora')
    def __str__(self):
        return f"Turno {self.veterinario} - {self.fecha} - {self.hora}"

        