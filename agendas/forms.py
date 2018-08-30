# -*- coding: utf-8 -*-
from django.db import models
#from django.forms import ModelForm
from django import forms
from models import *
from foros.models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class AgendaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
    	model = Agendas
    	exclude = ('user',)

class DocuForm(forms.ModelForm):
    class Meta:
    	model = Documentos
    	exclude = ('content_type', 'object_id', 'content_object',)