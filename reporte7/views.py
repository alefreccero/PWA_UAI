# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from cursadas.models import cursadas
from django import template
# Create your views here.

def showreport1(request):
    
	allcursadas = cursadas.objects.all()
		    
	contexto = {'allcursadas': allcursadas}
	#contexto = template.Context('allaulas': 'allaulas')
		    #return a response to your template and add query_results to the context
	return render(request, 'reporte7.html', contexto)

