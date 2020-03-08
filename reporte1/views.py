# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from reporte1.models import cursadasinaula
from django import template
# Create your views here.

def showreport1(request):
    
	allcursadassinaula = cursadasinaula.objects.all()
		    
	contexto = {'allcursadassinaula': allcursadassinaula}
	#contexto = template.Context('allaulas': 'allaulas')
		    #return a response to your template and add query_results to the context
	return render(request, 'reporte1.html', contexto)

