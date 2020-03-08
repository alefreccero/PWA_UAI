# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from aulas.models import aulas
from django import template
# Create your views here.

def showreport1(request):
    
	allaulas = aulas.objects.all()
		    
	contexto = {'allaulas': allaulas}
	#contexto = template.Context('allaulas': 'allaulas')
		    #return a response to your template and add query_results to the context
	return render(request, 'reporte6.html', contexto)

