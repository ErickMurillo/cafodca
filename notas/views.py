# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
from agendas.models import *
from foros.models import *
from foros.forms import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.forms import generic_inlineformset_factory

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
	contrapartes = Contraparte.objects.filter(id__in=[11,2,8,14])
	imagenes = Imagen.objects.order_by('-id')[:8]

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

@login_required
def crear_nota(request, template='admin/notas_form.html'):
	if request.method == 'POST':
		form = NotasForms(request.POST, files=request.FILES)
		form2 = FotoForm(data=request.POST, files=request.FILES)
		form3 = AdjuntoForm(data=request.POST, files=request.FILES)

		if form.is_valid() and form2.is_valid() and form3.is_valid():
			form_uncommited = form.save(commit=False)
			form_uncommited.user = request.user
			form_uncommited.save()

			form2_uncommited = form2.save(commit=False)
			form2_uncommited.content_object = form_uncommited
			form2_uncommited.save()

			form3_uncommited = form3.save(commit=False)
			form3_uncommited.content_object = form_uncommited
			form3_uncommited.save()

			# thread.start_new_thread(notify_all_notas, (form_uncommited,))
			return redirect('notas-personales')
	else:
		form = NotasForms()
		form2 = FotoForm()
		form3 = AdjuntoForm()

	return render(request, template, locals())
