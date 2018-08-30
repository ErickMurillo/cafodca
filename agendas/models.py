# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from foros.models import Documentos
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User
# from south.modelsinspector import add_introspection_rules
from ckeditor_uploader.fields import RichTextUploadingField

# add_introspection_rules ([], ["^ckeditor\.fields\.RichTextField"])

# Create your models here.

class Agendas(models.Model):
    evento = models.CharField(max_length=200)
    descripcion = RichTextUploadingField()
    inicio = models.DateField('Fecha de Inicio')
    final = models.DateField('Fecha de Finalización')
    publico = models.BooleanField()
    adjunto = GenericRelation(Documentos)
    user = models.ForeignKey(User)

    class Meta:
    	verbose_name_plural = "Agendas"

    def __unicode__(self):
    	return u'%s' % self.evento

    def get_absolute_url(self):
        return '/agendas/%d/' % (self.id,)


