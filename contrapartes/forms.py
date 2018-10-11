# -*- coding: UTF-8 -*-
from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from contrapartes.widgets import ColorPickerWidget
from django.forms import ModelMultipleChoiceField

class ContraparteForms(forms.ModelForm):
    temas = forms.CharField(widget=CKEditorUploadingWidget())
    siglas = forms.CharField(widget=forms.TextInput(attrs={'rel':"tooltip", 'title':"Siglas o nombre corto"}))
    generalidades = forms.CharField(widget=CKEditorUploadingWidget())
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'span7','rel':"tooltip", 'title':"Nombre completo de la contraparte"}))
    fundacion = forms.CharField(widget=forms.TextInput(attrs={'rel':"tooltip", 'title':"Año en que fue fundada la organización"}))
    contacto = forms.CharField(required=False,widget=forms.TextInput(attrs={'rel':"tooltip", 'title':"Nombre completo de la persona de contacto"}))
    telefono = forms.CharField(required=False,widget=forms.TextInput(attrs={'rel':"tooltip", 'title':"Formato ### - ######## "}))
    # sitio_web = forms.URLField(required=False,widget=forms.TextInput(attrs={'rel':"tooltip", 'title':"Con este formato http://www.dominio.com "}))
    # rss = forms.CharField(required=False,widget=forms.TextInput(attrs={'rel':"tooltip", 'title':"Dirección rss de contenido sindicado"}))
    # font_color = forms.CharField(required=False, widget=ColorPickerWidget, label="Color")

    class Meta:
        model = Contraparte
        exclude = ('user','sitio_web','rss','font_color')

class UserForm(ModelForm):
    class Meta:
	model = User
	fields = ('username', 'first_name', 'last_name', 'email')

class UserProfileForm(ModelForm):
    class Meta:
	model = UserProfile
	fields = ('avatar',)

class UserModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        #user_profile = UserProfile.objects.get(user__id=obj.pk)
        #print obj.userprofile.contraparte.siglas
        print dir(obj)
        return "%s" % (obj.username)

class MensajeForm(forms.ModelForm):
    user = UserModelMultipleChoiceField(queryset = User.objects.order_by('username'))
    class Meta:
        #widgets = {'user': forms.CheckboxSelectMultiple}
    	model = Mensajero
        exclude = ('usuario','fecha')

class RedesFrom(forms.ModelForm):
    class Meta:
        model = Redes
        fields = '__all__'
        exclude = ['organizacion',]
