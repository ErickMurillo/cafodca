# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import * 
from .forms import *
from notas.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.forms import generic_inlineformset_factory

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

@login_required
def crear_agenda(request,template='admin/agenda_form.html'):
	if request.method == 'POST':
		form = AgendaForm(request.POST, request.FILES)
		form1 = DocuForm(request.POST, request.FILES)

		if form.is_valid() and form1.is_valid():
			form_uncommited = form.save(commit=False)
			form_uncommited.user = request.user
			form_uncommited.save()
			if form1.cleaned_data['nombre_doc'] != '':
				form1_uncommitd = form1.save(commit=False)
				form1_uncommitd.content_object = form_uncommited
				form1_uncommitd.save()

			return redirect('agenda-personales')
	else:
		form = AgendaForm()
		form1 = DocuForm()

	return render(request, template, locals())

@login_required
def editar_agenda(request, id, template='admin/agenda_form.html'):
	agenda = get_object_or_404(Agendas, id=id)
	#agenda_type = ContentType.objects.get(app_label="foros",model="documentos")
	#docu = agenda_type.get_object_for_this_type(object_id=id)
	AgendaFormSet = generic_inlineformset_factory(Documentos, extra=2)
	form1 = AgendaFormSet(instance=agenda)

	if not agenda.user.userprofile.contraparte == request.user.userprofile.contraparte:
		return HttpResponse("Usted no puede editar esta Agenda")

	if request.method == 'POST':
		form = AgendaForm(request.POST, files=request.FILES, instance = agenda)
		form1 = AgendaFormSet(data=request.POST, files=request.FILES, instance = agenda)
		if form.is_valid() and form1.is_valid():
			form_uncommited = form.save(commit=False)
			form_uncommited.user = request.user
			form_uncommited.save()

			#form1_uncommitd = form1.save(commit=False)
			#form1_uncommitd.content_object = form_uncommited
			#form1_uncommitd.save()
			form1.save()
			return redirect('agenda-personales')
	else:
		form = AgendaForm(instance=agenda)
		form1 = AgendaFormSet(instance=agenda)
		
	return render(request, template, locals())

@login_required
def borrar_agenda(request, id):
	agenda = get_object_or_404(Agendas, pk=id)

	if agenda.user == request.user or request.user.is_superuser:
		agenda.delete()
		return redirect('/foros/privado/agenda/')
	else:
		return redirect('/')