# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from reporte5.forms import reporteForm
from asignador.models import planificacion
from django import template
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
# Create your views here.

def reporte5(request):

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = reporteForm(request.POST)
		# check whether it's valid:
		if form.is_valid():

			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
			#aula = (data.get('Aula') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
			#carrera = data.get('carrera') #esto refiere al nombre que definimos en el form.py
			aula = data.get('Aula') #esto refiere al nombre que definimos en el form.py
			dia = data.get('dia') #esto refiere al nombre que definimos en el form.py
			nombremat = data.get('nombremat') #esto refiere al nombre que definimos en el form.py
			turno = data.get('turno') #esto refiere al nombre que definimos en el form.py
			piso = data.get('piso')
			comision = data.get('comision')
			cluster = Cluster(['127.0.0.1'])
			session = cluster.connect()
			session.set_keyspace('dbpwa')
			#query = session.prepare('SELECT * FROM planificacion WHERE aula=? AND carrera=? AND comision=? AND dia=? AND nombremat=? AND piso=? AND turno=? ALLOW FILTERING;')#PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
			query = session.prepare('SELECT * FROM planificacion WHERE comision=? ALLOW FILTERING;') #PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
			#rows = session.execute(query, [aula, carrera, comision, dia, nombremat, piso, turno])

			cronograma = session.execute(query, [comision])


			session.shutdown()
			contexto = {'cronograma': cronograma}
			#contexto = template.Context('allaulas': 'allaulas')
					#return a response to your template and add query_results to the context
					
			return render(request, 'reporte2.html', contexto)
	else:
		form = reporteForm()
	return render(request, 'reporte5.html', {'form': form})