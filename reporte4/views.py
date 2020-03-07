# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from reporte4.forms import reporteForm
from asignador.models import planificacion
from django import template
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from aulas.models import aulas


# Create your views here.

def reporte4(request):

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		#form = reporteForm(request.POST)
		# check whether it's valid:
		# if form.is_valid():

			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
		#data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
		#aula = (data.get('Aula') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
		#carrera = data.get('carrera') #esto refiere al nombre que definimos en el form.py
		aula = request.POST.get('aula') #esto refiere al nombre que definimos en el form.py
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.set_keyspace('dbpwa')
		query = session.prepare('SELECT * FROM planificacion WHERE aula=? ALLOW FILTERING;') #PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
		cronograma = session.execute(query, [aula])
		contexto = {'cronograma': cronograma}

		return render(request, 'reporte4-1.html', contexto)
	else:

		# form = reporteForm()
		allaulas = aulas.objects.all()

		contexto = {'allaulas': allaulas}
		return render(request, 'reporte4.html', contexto)
