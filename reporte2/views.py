# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from asignador.models import planificacion
from django import template
# Create your views here.

def reporte_planificador(request):
    
	cronograma = planificacion.objects.all()
		    
	contexto = {'cronograma': cronograma}
	#contexto = template.Context('allaulas': 'allaulas')
		    #return a response to your template and add query_results to the context
			
	return render(request, 'reporte2.html', contexto)

