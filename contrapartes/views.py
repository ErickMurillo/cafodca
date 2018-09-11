# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

# Create your views here.
@login_required
def editar_contraparte(request, id, template='admin/editar_contraparte.html'):
	contra = get_object_or_404(Contraparte, id=id)
	FormSetInit = inlineformset_factory(Contraparte, Redes, form=RedesFrom,extra=11,max_num=11)

	if request.method == 'POST':
		form = ContraparteForms(data=request.POST,instance=contra,files=request.FILES)
		formset = FormSetInit(request.POST,request.FILES,instance=contra)

		if form.is_valid() and formset.is_valid():
			form_uncommited = form.save(commit=False)
			form_uncommited.user = request.user
			form_uncommited.save()

			formset.save()

			return redirect('ver-perfil')
	else:
		form = ContraparteForms(instance=contra)
		formset = FormSetInit(instance=contra)

	return render(request, template, locals())
