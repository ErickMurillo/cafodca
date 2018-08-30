# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import *
from models import *
from foros.models import *
from foros.forms import *

class DocumentosInline(GenericTabularInline):
    model = Documentos
    extra = 1

class ImagenInline(GenericTabularInline):
    model = Imagen
    extra = 1

class VideosInline(GenericTabularInline):
    model = Videos
    extra = 1

class AudiosInline(GenericTabularInline):
    model = Audios
    extra = 1

class ForoAdmin(admin.ModelAdmin):
    inlines = [DocumentosInline, ImagenInline, 
              VideosInline, AudiosInline]
    form = ForosForm
    list_display = ['nombre','creacion','contraparte',
                    '__documento__','__fotos__', '__video__',
                    '__audio__']
    date_hierarchy = 'creacion'

class AportesAdmin(admin.ModelAdmin):
    inlines = [DocumentosInline, ImagenInline, 
              VideosInline, AudiosInline]
    form = AporteForm
    list_display = ['__unicode__','fecha','user',
                    '__documento__','__fotos__', 
                    '__video__','__audio__']
    list_filter = ['user','fecha']
    date_hierarchy = 'fecha'

class ComentariosAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'aporte')
    form = ComentarioForm

admin.site.register(Foros, ForoAdmin)
admin.site.register(Aportes, AportesAdmin)
admin.site.register(Comentarios, ComentariosAdmin)
admin.site.register(Documentos)
admin.site.register(Imagen)
admin.site.register(Videos)
admin.site.register(Audios)
# Register your models here.
