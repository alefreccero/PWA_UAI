# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from aulas.models import aulas
from django import template
# Create your views here.

def reporte_filtrado(request):
	if request.method == 'POST':
		if form.is_valid():
			return render(request, 'reporte3.html', contexto)
	else:
		allaulas = aulas.objects.all()
		contexto = {'allaulas': allaulas}
		return render(request,'reporte3.html', contexto)
