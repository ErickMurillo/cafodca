# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from agendas.models import *
from django.shortcuts import render_to_response, get_object_or_404
import datetime

# Create your views here.
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def index(request,template='index.html'):

	notas = Notas.objects.all().order_by('-fecha','-id')[:6]
	notas2 = Notas.objects.all().order_by('-fecha','-id')[1:9]
	hoy = datetime.date.today()
	eventos = Agendas.objects.filter(inicio__gte = hoy,publico=True).order_by('-inicio','-hora_inicio')[:4]
	paises = Pais.objects.all()
	contrapartes = Contraparte.objects.all()

	return render(request, template, locals())

def list_notas(request, template='blog-list.html'):
	object_list = Notas.objects.order_by('-id')
	ultimas_notas = Notas.objects.order_by('-id')[:3]
	paises = Pais.objects.all()

	return render(request, template, locals())

def nota_detail(request,id, template='blog-single.html'):
	object = get_object_or_404(Notas, id=id)
	ultimas_notas = Notas.objects.exclude(id = id).order_by('-id')[:3]
	paises = Pais.objects.all()

	return render(request, template, locals())

def lista_notas_pais(request,id, template='blog-list.html'):
	object_list = Notas.objects.filter(user__userprofile__contraparte__pais = id).order_by('-id')
	ultimas_notas = Notas.objects.order_by('-id')[:3]
	paises = Pais.objects.all()

	return render(request, template, locals())
