# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect

from .forms import cursadasForm
import uuid
#IMPORTS PARA QUE FUNCIONE EL DRIVER CON CASSANDRA
from django.contrib import messages
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
#from models import ExampleModel
from cursadas.models import cursadas

from django.db import connection
from django.http import HttpResponse 

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = cursadasForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
            cantalumnos = data.get('CantAlumnos') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
            carrera = data.get('carrera') #esto refiere al nombre que definimos en el form.py
            comision = data.get('comision') #esto refiere al nombre que definimos en el form.py
            #horario = data.get('horario') #esto refiere al nombre que definimos en el form.py
            nombremat = data.get('nombremat') #esto refiere al nombre que definimos en el form.py
            turno = data.get('turno') #esto refiere al nombre que definimos en el form.py
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            query = session.prepare('SELECT * FROM cursadas WHERE comision=? AND turno=? AND carrera=? AND nombremat=? ALLOW FILTERING;')#PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
            rows = session.execute(query, [comision, turno, carrera, nombremat]) #EJECUTO LA QUERY Y LE PASO LAS VARIABLES PARA FILTRAR IMPORTANTE QUE ESTEN ENTRE CORCHETES
            existen = [] #CREO UN ARRAY
            for row in rows:
                existen.append(row) #LLENO EL ARRAY CON LAS FILAS
            cluster.shutdown() # Cierro La conexion
            if len(existen) > 0: #VERIFICO SI ESE TURNO PARA ESA COMISION YA ESTA USADO
                messages.error(request, "La carrera {} comision {} ya tiene una materia {} asignada en el turno {}".format(carrera, comision, nombremat, turno)) 
                
                
            else:
                cursadita = cursadas() # Instancio un objeto aula
                cursadita.nombremat = nombremat # asigno los valores del form en la prop del objeto instanciado en el paso anterior
                cursadita.carrera= carrera # asigno los valores del form en la prop del objeto instanciado en el paso anterior
                cursadita.turno=turno
                cursadita.cursada_id= uuid.uuid1()
                cursadita.comision= comision
                cursadita.cantalumnos= cantalumnos
                cursadita.save() # salvo el objeto en la DB
                messages.success(request, "Se ha creado exitosamente la cursada {} de la carrera {} en el turno {} para la comisión {} con {} inscriptos".format(nombremat, carrera, turno,  comision, cantalumnos))  
                
            

    # if a GET (or any other method) we'll create a blank form
    else:

        form = cursadasForm()


    return render(request, 'cursadas.html', {'form': form})
