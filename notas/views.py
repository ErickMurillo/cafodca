# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from agendas.models import *
from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def index(request,template='index.html'):

	notas = Notas.objects.all().order_by('-fecha','-id')[:6]
	notas2 = Notas.objects.all().order_by('-fecha','-id')[1:9]
	evento = Agendas.objects.filter(publico=True).order_by('-inicio')[:4]
	paises = Pais.objects.all()
	contrapartes = Contraparte.objects.all()

	return render(request, template, locals())

def nota_detail(request,id, template='blog-single.html'):
	object = get_object_or_404(Notas, id=id)

	return render(request, template, locals())
