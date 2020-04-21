from django.conf.urls import url
from django.views.generic import ListView, DetailView
from models import Notas
from .views import *

urlpatterns = [
    url(r'^$', list_notas,name='notas_list'),
    # url(r'^$', 'lista_notas', name="notas_list"),
    url(r'^pais/(?P<id>\d+)/$', lista_notas_pais, name="notas_list_pais"),
    url(r'^coparte/(?P<id>\d+)/$', lista_notas_copartes, name="notas_list_copartes"),
    # url(r'^ver/(?P<id>\d+)/$', 'comentar_nota', name='comentar-nota'),
    url(r'^(?P<id>\d+)/$', nota_detail, name='notas-detail'),
    url(r'^crear/$', crear_nota, name="crear-nota"),
    # url(r'^editar/(?P<id>\d+)/$', 'editar_nota', name='editar-nota'),
    # url(r'^borrar/(?P<id>\d+)/$', 'borrar_nota', name='borrar-nota'),
    url(r'^imagenes/$', ver_imagenes, name="imagenes-nota"),
    url(r'^videos/$', ver_videos, name="videos-nota"),
    ]
