# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import * 
from notas.models import *

# Create your views here.
def agenda_list(request, template='events-list.html'):
	object_list = Agendas.objects.order_by('-id')
	ultimas_notas = Notas.objects.order_by('-id')[:3]
	paises = Pais.objects.all()

	return render(request, template, locals())

def agenda_detail(request, id, template='event-single.html'):
	object = get_object_or_404(Agendas, id=id)
	ultimas_notas = Notas.objects.order_by('-id')[:3]
	paises = Pais.objects.all()

	return render(request, template, locals())

def lista_events_pais(request,id, template='events-list.html'):
	object_list = Agendas.objects.filter(user__userprofile__contraparte__pais = id).order_by('-id')
	ultimas_notas = Notas.objects.order_by('-id')[:3]
	paises = Pais.objects.all()

	return render(request, template, locals())
