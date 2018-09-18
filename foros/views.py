# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from agendas.models import *
from notas.models import *
from contrapartes.models import *
from notas.forms import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.contenttypes.forms import generic_inlineformset_factory

# Create your views here.
@login_required
def perfil(request, template='admin/perfil.html'):
	usuario = request.user.id
	user_profile = get_object_or_404(UserProfile, user = usuario)
	contraparte = get_object_or_404(Contraparte, id = user_profile.contraparte.id)
	
	foros = Foros.objects.filter(contraparte_id=request.user.id)
	agendas = Agendas.objects.filter(user_id=request.user.id)

	return render(request, template, locals())

@login_required
def notas_personales(request, template='admin/notas.html'):
	object_list = Notas.objects.filter(user_id=request.user.id)

	return render(request, template, locals())

@login_required
def notas_personales_editar(request, id, template='admin/notas_form.html'):
	object = get_object_or_404(Notas, id=id)
	ForoImgFormSet = generic_inlineformset_factory(Imagen, extra=5, max_num=5)
	ForoDocuFormSet = generic_inlineformset_factory(Documentos, extra=5, max_num=5)

	if request.method == 'POST':
		form = NotasForms(request.POST, request.FILES, instance=object)
		form2 = ForoImgFormSet(data=request.POST, files=request.FILES, instance=object)
		form3 = ForoDocuFormSet(data=request.POST, files=request.FILES, instance=object)
		
		if form.is_valid() and form2.is_valid() and form3.is_valid():
			form_uncommited = form.save()
			form_uncommited.user = request.user
			form_uncommited.save()

			form2.save()
			form3.save()
			
			return redirect('notas-personales')
	else:
		form = NotasForms(instance=object)
		form2 = ForoImgFormSet(instance=object)
		form3 = ForoDocuFormSet(instance=object)

	return render(request, template, locals())

@login_required
def eliminar_notas_contraparte(request, id):
	nota = Notas.objects.filter(id = id).delete()
	return redirect('notas-personales')

@login_required
def agenda_personales(request, template='admin/agendas.html'):
    object_list = Agendas.objects.filter(user_id=request.user.id)

    return render(request, template, locals())