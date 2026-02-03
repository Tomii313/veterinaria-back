from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Animal(models.Model):

    estados = [
        ("TRATAMIENTO", "En Tratamiento"),
        ("VACUNACION", "Vacunación Pendiente"),
        ("INTERNACION", "Internacion"),
        ("DESPARASITACION", "Desparasitacion"),
        ("SANO", "Sano"),
        ("FALLECIDO", "Fallecido")
    ]
    raza = models.CharField(max_length=100, null=True, blank=True)
    peso = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    edad = models.IntegerField(null=True, blank=True)
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=100, null=True, blank=True)
    especie = models.CharField(max_length=50, null=True, blank=True)
    duenio = models.ForeignKey('duenios.Duenio', on_delete=models.CASCADE, related_name="mascotas", null=True, blank=True)
    estado = models.CharField(max_length=100, choices=estados, default="TRATAMIENTO")
    """ veterinario = models.ForeignKey('veterinarios.Veterinario', on_delete=models.CASCADE) """

    def __str__(self):
        return f"{self.nombre} - {self.especie} {self.edad} AÑOS"


class Estudios(models.Model):

    
    TIPO = [
        ('RX', 'Radiografía'),
        ('SANGRE', 'Análisis de Sangre'),
        ('ECO', 'Ecografía'),
        ("ORINA", "Análisis de Orina"),
        ('OTRO', 'Otro'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="estudios")
    tipo = models.CharField(max_length=100, choices=TIPO)
    informe = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    archivo = models.FileField(upload_to="estudios_pdf/")


    def __str__(self):
        return f"{self.tipo} - {self.fecha}"

    class Meta:
        verbose_name ="Estudio"
        verbose_name_plural = "Estudios"
    
