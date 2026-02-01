from django.db import models

# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre  

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"