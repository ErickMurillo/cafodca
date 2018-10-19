# -*- coding: utf-8 -*-
from django.db import models
from solo.models import SingletonModel

# Create your models here.

class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    maintenance_mode = models.BooleanField(default=False)
    acerca = models.TextField()

    def __unicode__(self):
        return u"Sitio Configuración"

    class Meta:
        verbose_name = "Sitio Configuración"


class FotosPortada(models.Model):
    sitio = models.ForeignKey(SiteConfiguration, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    descripcion = models.TextField()
    foto = models.FileField(upload_to='fotoportada/')

    def __unicode__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Foto de portada'
        verbose_name_plural = 'Fotos de las portadas'
