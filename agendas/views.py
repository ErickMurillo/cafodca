# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *

# Create your views here.
def agenda_list(request, template='events-list.html'):
	object_list = Agendas.objects.order_by('-id')

	return render(request, template, locals())
