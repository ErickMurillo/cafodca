from django.conf.urls import url
from django.views.generic import ListView, DetailView
from models import Agendas
from .views import *

urlpatterns = [
    url(r'^$', agenda_list, name="agenda-list"),
    url(r'^(?P<id>\d+)/$', agenda_detail, name='agenda-detail'),
    url(r'^pais/(?P<id>\d+)/$', lista_events_pais, name="events_list_pais"),
    url(r'^crear/$', crear_agenda, name="crear-agenda"),
    url(r'^editar/(?P<id>\d+)/$', editar_agenda, name='editar-agenda'),
    url(r'^borrar/(?P<id>\d+)/$', borrar_agenda, name='borrar-agenda'),
    # url(r'^calendario/$', calendario, name='calendario'),
    # url(r'^calendario/(?P<id>\d+)/$', 'calendario', name='calendario'),
    # url(r'^eventos/(?P<id>\d+)/$', 'calendario_publico', name='calendario_publico'),
    # url(r'^eventos/$', 'calendario_publico', name='calendario_publico'),
    # url(r'^calendar/$', 'calendario_full_contraparte', name='calendario-full-contraparte'),
    # url(r'^calendar/(?P<id>\d+)/$', 'calendario_full_contraparte', name='calendario-full-contraparte'),
    ]