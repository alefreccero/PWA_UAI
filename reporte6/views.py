# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from reporte6.models import aulasinuso
from django import template
# Create your views here.

def showreport1(request):
    
	allaulasinuso = aulasinuso.objects.all()
		    
	contexto = {'allaulasinuso': allaulasinuso}
	#contexto = template.Context('allaulas': 'allaulas')
		    #return a response to your template and add query_results to the context
	return render(request, 'reporte6.html', contexto)

