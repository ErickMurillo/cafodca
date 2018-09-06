# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from agendas.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def perfil(request, template='admin/perfil.html'):
    foros = Foros.objects.filter(contraparte_id=request.user.id)
    agendas = Agendas.objects.filter(user_id=request.user.id)

    return render(request, template, locals())
