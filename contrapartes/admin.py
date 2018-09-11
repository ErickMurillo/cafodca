# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .forms import *

class RedesInline(admin.TabularInline):
	model = Redes
	extra = 1

class ContraparteAdmin(admin.ModelAdmin):
	form = ContraparteForms
	inlines = [RedesInline,]
    #class Media:
    #    js = ['../files/js/tiny_mce/tiny_mce.js',
    #          '../files/js/editores/textareas.js',]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','__fecha_registro__']

admin.site.register(Pais)
admin.site.register(Contraparte, ContraparteAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Mensajero)
