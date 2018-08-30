# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *
from agendas.forms import *
from django.contrib.contenttypes.admin import *
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
 
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
 
class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = FlatPage
        fields = '__all__'
 
 
class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm
 
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

class DocumentosInline(GenericTabularInline):
    model = Documentos
    extra = 1

class AgendasAdmin(admin.ModelAdmin):
    inlines = [DocumentosInline,]
    form = AgendaForm
    #class Media:
    #    js = ['../files/js/tiny_mce/tiny_mce.js',
    #          '../files/js/editores/textareas.js',]
    list_display = ['__unicode__','inicio','user']
    list_filter = ['user','inicio']
    date_hierarchy = 'inicio'
