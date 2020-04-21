# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
import thread

from .models import *
from notas.models import Notas
from foros.models import Foros, Aportes, Comentarios
from agendas.models import Agendas

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


def detalle_contraparte(request,id):
    contra = get_object_or_404(Contraparte, id=id)
    notas = Notas.objects.filter(user__userprofile__contraparte__id=id).order_by('-fecha')[:5]
    return render(request, 'contraparte_detail.html', locals(),)

@login_required
def editar_usuario_perfil(request):
    #usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=request.user)
        form1 = UserProfileForm(data=request.POST, instance=request.user.userprofile, files=request.FILES)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            #form_uncommited = form.save(commit=False)
            #form_uncommited.user = request.user
            #form_uncommited.save()

            return HttpResponseRedirect('/foros/perfil')
    else:
        form = UserForm(instance=request.user)
        form1 = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'contrapartes/editar_usuario.html', locals())

@login_required
def enviar_mensaje(request):
    mensaje = Mensajero.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(mensaje, 5)
    page = request.GET.get('page')
    try:
        mensajes = paginator.page(page)
    except PageNotAnInteger:
        mensajes = paginator.page(1)
    except EmptyPage:
        mensajes = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        form.fields['user'].queryset = User.objects.exclude(id=request.user.id)
        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.usuario = request.user
            form_uncommited.save()
            form.save_m2m()

            thread.start_new_thread(notify_user_mensaje, (form_uncommited, ))
            guardado='ok'

            return HttpResponseRedirect('/contrapartes/mensaje/ver/?guardado=ok')

    else:
        form = MensajeForm()
        form.fields['user'].queryset = User.objects.exclude(id=request.user.id)
        guardado=0
    return render(request, 'contrapartes/mensaje.html', locals())

def notify_user_mensaje(mensaje):
    site = Site.objects.get_current()
    contenido = render_to_string('contrapartes/notify_new_mensaje.html', {
                                   'mensajes': mensaje,
                                   'url': '%s/contrapartes/mensaje/ver/' % (site,)
                                    })
    msg = EmailMultiAlternatives('Nuevo mensaje CAFOD', contenido, 'cafodca@gmail.com', [user.email for user in mensaje.user.all() if user.email])
    msg.attach_alternative(contenido, "text/html")
    msg.send()
    #send_mail('Nuevo mensaje CAFOD', contenido, 'cafodca@gmail.com', [user.email for user in mensaje.user.all() if user.email])

@login_required
def estadisticas(request):
    total = {}

    lista_noticias = {}
    lista_foros = {}
    lista_aportes = {}
    lista_comentarios = {}

    for obj in Contraparte.objects.all():
        noticias = Notas.objects.filter(user__userprofile__contraparte=obj).count()
        lista_noticias[obj.siglas] = noticias
        foros = Foros.objects.filter(contraparte__userprofile__contraparte=obj).count()
        lista_foros[obj.siglas] = foros
        aportes = Aportes.objects.filter(user__userprofile__contraparte=obj).count()
        lista_aportes[obj.siglas] = aportes
        comentarios = Comentarios.objects.filter(usuario__userprofile__contraparte=obj).count()
        lista_comentarios[obj.siglas] = comentarios

    for usuario in User.objects.all():
        foro = Foros.objects.filter(contraparte=usuario).count()
        nota = Notas.objects.filter(user=usuario).count()
        aporte = Aportes.objects.filter(user=usuario).count()
        comentario = Comentarios.objects.filter(usuario=usuario).count()
        #Estadisticas sobre documentos,imagenes,videos,audios

        lista_documentos_notas = []
        lista_imagenes_notas = []
        for documentos in Notas.objects.filter(user=usuario):
            for numero in documentos.adjuntos.all():
                lista_documentos_notas.append(numero)
            for foto in documentos.fotos.all():
                lista_imagenes_notas.append(foto)

        lista_documentos_eventos = []
        for eventos in Agendas.objects.filter(user=usuario):
            for numero in eventos.adjunto.all():
                lista_documentos_eventos.append(numero)

        lista_documentos_foros = []
        lista_imagenes_foros = []
        lista_videos_foros = []
        lista_audios_foros = []
        for foros in Foros.objects.filter(contraparte=usuario):
            for numero in foros.documentos.all():
                lista_documentos_foros.append(numero)
            for imagen in foros.fotos.all():
                lista_imagenes_foros.append(imagen)
            for video in foros.video.all():
                lista_videos_foros.append(video)
            for audio in foros.audio.all():
                lista_audios_foros.append(audio)

        lista_documentos_aporte = []
        lista_imagen_aporte = []
        lista_videos_aporte = []
        lista_audios_aporte = []
        for aportes in Aportes.objects.filter(user=usuario):
            for numero in aportes.adjuntos.all():
                lista_documentos_aporte.append(numero)
            for imagen in aportes.fotos.all():
                lista_imagen_aporte.append(imagen)
            for video in aportes.video.all():
                lista_videos_aporte.append(video)
            for audio in aportes.audio.all():
                lista_audios_aporte.append(audio)


        documentos = len(lista_documentos_notas) + len(lista_documentos_eventos) + \
        len(lista_documentos_foros) + len(lista_documentos_aporte)
        imagenes = len(lista_imagenes_notas) + len(lista_imagenes_foros) + \
        len(lista_imagen_aporte)
        #documentos = foro2.aggregate(documentos=Count('documentos'))['documentos']
        #imagenes = aporte2.aggregate(imagenes=Count('fotos'))['imagenes']
        videos = len(lista_videos_foros) + len(lista_videos_aporte)
        audios = len(lista_audios_foros) + len(lista_audios_aporte)
        total[usuario] = (nota,foro,aporte,comentario,documentos,imagenes,videos,audios)

    return render(request, 'contrapartes/estadisticas.html', locals())
