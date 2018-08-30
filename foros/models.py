# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
# from south.modelsinspector import add_introspection_rules
# from tagging.models import Tag
from tagging.fields import TagField
# from taggit_autosuggest.managers import TaggableManager
from django.contrib.auth.models import User
#from contrapartes.models import Usuarios
# from thumbs import ImageWithThumbsField
from sorl.thumbnail import ImageField
from utils import *
import datetime
# from south.modelsinspector import add_introspection_rules
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from embed_video.fields import EmbedVideoField

# add_introspection_rules ([], ["^ckeditor\.fields\.RichTextField"])
# add_introspection_rules ([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])

# Create your models here.

class Imagen(models.Model):
    ''' Modelo generico para subir imagenes en todos los demas app :)'''
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    nombre_img = models.CharField("Nombre",max_length=200, null=True, blank=True)
    foto = ImageField("Foto",upload_to=get_file_path,null=True, blank=True)
    tags_img = TagField("Tags",help_text='Separar elementos con "," ', blank=True)
    fileDir = 'fotos/'
    class Meta:
    	verbose_name_plural = "Imágenes"

    def __unicode__(self):
    	return self.nombre_img

class Documentos(models.Model):
    ''' Modelo generico para subir los documentos en distintos app'''
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    nombre_doc = models.CharField("Nombre",max_length=200, null=True, blank=True)
    adjunto = models.FileField("Adjunto",upload_to=get_file_path, null=True, blank=True)
    tags_doc = TagField("Tags",help_text='Separar elementos con "," ', blank=True)

    fileDir = 'documentos/'

    class Meta:
    	verbose_name_plural = "Documentos"

    def __unicode__(self):
    	return self.nombre_doc

class Videos(models.Model):
    ''' Modelo generico para subir videos en todos los app'''
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    nombre_video = models.CharField(max_length=200, null=True, blank=True)
    url = EmbedVideoField(null=True, blank=True)
    tags_vid = TagField(help_text='Separar elementos con "," ', blank=True)

    class Meta:
    	verbose_name_plural = "Videos"

    def __unicode__(self):
    	return self.nombre_video

class Audios(models.Model):
    '''' Modelo generico para subir audios en todos los demas app '''
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    nombre_audio = models.CharField(max_length=200, null=True, blank=True)
    audio = models.FileField(upload_to=get_file_path, null=True, blank=True)
    tags_aud = TagField(help_text='Separar elementos con "," ', blank=True)

    fileDir = 'audios/'

    class Meta:
    	verbose_name_plural = "Audios"

    def __unicode__(self):
    	return self.nombre_audio

class Foros(models.Model):
    nombre = models.CharField(max_length=200)
    creacion = models.DateField(auto_now_add=True)
    apertura = models.DateField('Apertura y recepción de aportes')
    cierre = models.DateField('Cierre de aportes')
    fecha_skype = models.DateField('Propuesta de reunión skype')
    memoria = models.DateField('Propuesta entrega de memoria')
    contenido = RichTextUploadingField()
    contraparte = models.ForeignKey(User)
    documentos = GenericRelation(Documentos)
    fotos = GenericRelation(Imagen)
    video = GenericRelation(Videos)
    audio = GenericRelation(Audios)

    class Meta:
    	verbose_name_plural = "Foros"
        ordering = ['-creacion']

    def __unicode__(self):
    	return self.nombre

    def __documento__(self):
        lista = []
        for obj in self.documentos.all():
            lista.append(obj)
        return lista

    def __fotos__(self):
        lista = []
        for obj in self.fotos.all():
            lista.append(obj)
        return lista

    def __video__(self):
        lista = []
        for obj in self.video.all():
            lista.append(obj)
        return lista

    def __audio__(self):
        lista = []
        for obj in self.audio.all():
            lista.append(obj)
        return lista

    def get_absolute_url(self):
        return "/foros/ver/%d" % (self.id)

class Aportes(models.Model):
    foro = models.ForeignKey(Foros)
    fecha = models.DateField(auto_now_add=True)
    contenido = RichTextUploadingField()
    user = models.ForeignKey(User)
    adjuntos = GenericRelation(Documentos)
    fotos = GenericRelation(Imagen)
    video = GenericRelation(Videos)
    audio = GenericRelation(Audios)

    class Meta:
        verbose_name_plural = "Aportes"

    def __unicode__(self):
        return self.foro.nombre
        
    def __documento__(self):
        lista = []
        for obj in self.adjuntos.all():
            lista.append(obj)
        return lista

    def __fotos__(self):
        lista = []
        for obj in self.fotos.all():
            lista.append(obj)
        return lista

    def __video__(self):
        lista = []
        for obj in self.video.all():
            lista.append(obj)
        return lista

    def __audio__(self):
        lista = []
        for obj in self.audio.all():
            lista.append(obj)
        return lista

class Comentarios(models.Model):
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    comentario = RichTextUploadingField()
    aporte = models.ForeignKey(Aportes)

    class Meta:
        verbose_name_plural = "Comentarios"

    def __unicode__(self):
        return self.usuario.username
