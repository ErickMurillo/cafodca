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
from tagging.models import Tag
from tagging.models import TaggedItem

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

@login_required
def documento(request, template='admin/documentos.html'):
	documentos = Documentos.objects.all()
	tags = []
	for docu in Documentos.objects.all():
		for tag in Tag.objects.filter(name=docu.tags_doc):
			tags.append(tag)

	query = request.GET.get('q', '')
	if query:
		result_documento = Documentos.objects.filter(nombre_doc__icontains=query)
		result_tags = Tag.objects.filter(name__icontains=query)
		lista = []
		tags_lista = []
		for n in result_documento:
			lista.append(n)
		for rtag in result_tags:
			TaggedItems = TaggedItem.objects.get_by_model(Documentos, rtag.name)
			if not rtag.items.all().count() == 0:
				li = []
				for it in rtag.items.all():
					if it.object:
						li.append(it)
				tags_lista.append({'name':rtag.name, 'count': len(li)})
			for item in TaggedItems:
				lista.append(item)
		#tags.sort(key=operator.itemgetter('count'), reverse=True)
		documentos = list(set(lista))

	return render(request, template, locals())

@login_required
def multimedia_fotos(request, template='admin/fotos.html'):
	imagenes = Imagen.objects.all()
	tags = []
	for docu in Imagen.objects.all():
		for tag in Tag.objects.filter(name=docu.tags_img):
			tags.append(tag)

	query = request.GET.get('q', '')
	if query:
		result_fotos = Imagen.objects.filter(nombre_img__icontains=query)
		result_tags = Tag.objects.filter(name__icontains=query)
		lista = []
		tags_lista = []
		for n in result_fotos:
			lista.append(n)
		for rtag in result_tags:
			TaggedItems = TaggedItem.objects.get_by_model(Imagen, rtag.name)
			if not rtag.items.all().count() == 0:
				li = []
				for it in rtag.items.all():
					if it.object:
						li.append(it)
				tags_lista.append({'name':rtag.name, 'count': len(li)})
			for item in TaggedItems:
				lista.append(item)
		#tags.sort(key=operator.itemgetter('count'), reverse=True)
		imagenes = list(set(lista))

	return render(request, template, locals())

@login_required
def multimedia_videos(request, template='admin/videos.html'):
	videos = Videos.objects.all()
	tags = []
	for docu in Videos.objects.all():
		for tag in Tag.objects.filter(name=docu.tags_vid):
			tags.append(tag)

	query = request.GET.get('q', '')
	if query:
		result_fotos = Videos.objects.filter(nombre_video__icontains=query)
		result_tags = Tag.objects.filter(name__icontains=query)
		lista = []
		tags_lista = []
		for n in result_fotos:
			lista.append(n)
		for rtag in result_tags:
			TaggedItems = TaggedItem.objects.get_by_model(Videos, rtag.name)
			if not rtag.items.all().count() == 0:
				li = []
				for it in rtag.items.all():
					if it.object:
						li.append(it)
				tags_lista.append({'name':rtag.name, 'count': len(li)})
			for item in TaggedItems:
				lista.append(item)
		#tags.sort(key=operator.itemgetter('count'), reverse=True)
		videos = list(set(lista))

	return render(request, template, locals())

@login_required
def multimedia_audios(request, template='admin/audios.html'):
	audios = Audios.objects.all()
	tags = []
	for docu in Audios.objects.all():
		for tag in Tag.objects.filter(name=docu.tags_aud):
			tags.append(tag)

	query = request.GET.get('q', '')
	if query:
		result_fotos = Videos.objects.filter(nombre_aud__icontains=query)
		result_tags = Tag.objects.filter(name__icontains=query)
		lista = []
		tags_lista = []
		for n in result_fotos:
			lista.append(n)
		for rtag in result_tags:
			TaggedItems = TaggedItem.objects.get_by_model(Videos, rtag.name)
			if not rtag.items.all().count() == 0:
				li = []
				for it in rtag.items.all():
					if it.object:
						li.append(it)
				tags_lista.append({'name':rtag.name, 'count': len(li)})
			for item in TaggedItems:
				lista.append(item)
		#tags.sort(key=operator.itemgetter('count'), reverse=True)
		audios = list(set(lista))

	return render(request, template, locals())

### Foros  ###
@login_required
def crear_foro(request):
    if request.method == 'POST':
        form = ForosForm(request.POST)
        form2 = ImagenForm(request.POST, request.FILES)
        form3 = DocumentoForm(request.POST, request.FILES)
        form4 = VideoForm(request.POST)
        form5 = AudioForm(request.POST, request.FILES)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.contraparte = request.user
            form_uncommited.save()
            if form2.cleaned_data['nombre_img'] != '':
                form2_uncommitd = form2.save(commit=False)
                form2_uncommitd.content_object = form_uncommited
                form2_uncommitd.save()
            if form3.cleaned_data['nombre_doc'] != '':
                form3_uncommitd = form3.save(commit=False)
                form3_uncommitd.content_object = form_uncommited
                form3_uncommitd.save()
            if form4.cleaned_data['nombre_video'] != '':
                form4_uncommitd = form4.save(commit=False)
                form4_uncommitd.content_object = form_uncommited
                form4_uncommitd.save()
            if form5.cleaned_data['nombre_audio'] != '':
                form5_uncommitd = form5.save(commit=False)
                form5_uncommitd.content_object = form_uncommited
                form5_uncommitd.save()

            thread.start_new_thread(notify_all_foro, (form_uncommited,))

            return HttpResponseRedirect('/foros')

    else:
        form = ForosForm()
        form2 = ImagenForm()
        form3 = DocumentoForm()
        form4 = VideoForm()
        form5 = AudioForm()
    return render(request, 'foros/crear_foro.html', locals())


@login_required
def ver_foro(request, foro_id):
    discusion = get_object_or_404(Foros, id=foro_id)

    if request.method == 'POST':
        form = AporteForm(request.POST)
        form2 = ImagenForm(request.POST, request.FILES)
        form3 = DocumentoForm(request.POST, request.FILES)
        form4 = VideoForm(request.POST)
        form5 = AudioForm(request.POST, request.FILES)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.foro = discusion
            form_uncommited.save()
            if form2.cleaned_data['nombre_img'] != '':
                form2_uncommitd = form2.save(commit=False)
                form2_uncommitd.content_object = form_uncommited
                form2_uncommitd.save()
            if form3.cleaned_data['nombre_doc'] != '':
                form3_uncommitd = form3.save(commit=False)
                form3_uncommitd.content_object = form_uncommited
                form3_uncommitd.save()
            if form4.cleaned_data['nombre_video'] != '':
                form4_uncommitd = form4.save(commit=False)
                form4_uncommitd.content_object = form_uncommited
                form4_uncommitd.save()
            if form5.cleaned_data['nombre_audio'] != '':
                form5_uncommitd = form5.save(commit=False)
                form5_uncommitd.content_object = form_uncommited
                form5_uncommitd.save()

            thread.start_new_thread(notify_all_aporte, (form_uncommited,))

            return HttpResponseRedirect('/foros/ver/%d' % discusion.id)
    else:
        form = AporteForm()
        form2 = ImagenForm()
        form3 = DocumentoForm()
        form4 = VideoForm()
        form5 = AudioForm()
    return render(request, 'foros/ver_foro.html',  locals())
