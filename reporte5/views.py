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
			comision = data.get('comision')
			cluster = Cluster(['127.0.0.1'])
			session = cluster.connect()
			session.set_keyspace('dbpwa')
			query = session.prepare('SELECT * FROM planificacion WHERE comision=? ALLOW FILTERING;') #PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
			cronograma = session.execute(query, [comision])


			session.shutdown()
			contexto = {'cronograma': cronograma}
					
			return render(request, 'reporte2.html', contexto)
	else:
		form = reporteForm()
	return render(request, 'reporte5.html', {'form': form})