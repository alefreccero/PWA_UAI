# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect

from .forms import AulasForm
import uuid
#IMPORTS PARA QUE FUNCIONE EL DRIVER CON CASSANDRA

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
#from models import ExampleModel
from aulas.models import aulas

from django.db import connection
from django.http import HttpResponse 

def crearaulas(nombre,capacidad,piso):
    #for dia in ['Lunes','Martes','Miercoles','Jueves','Viernes']:
        aulita = aulas() # Instancio un objeto aula
        aulita.aula_id = uuid.uuid1()
        aulita.nombre = nombre # asigno los valores del form en la prop del objeto instanciado en el paso anterior
        aulita.capacidad= capacidad # asigno los valores del form en la prop del objeto instanciado en el paso anterior
        aulita.piso=piso
        #aulita.dia= dia
        aulita.save() # salvo el objeto en la DB


def get_aula(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AulasForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
            aulanombre = data.get('aula') #aca extraigo los campos del form delñ data que definimos en la linea anterior, el parentisis refiere al nombre que definimos el campo en el form.py
            aulacapa = data.get('capacidad') #esto refiere al nombre que dEfinimos en el form.py
            aulapiso = data.get('piso')
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            query = session.prepare('SELECT * FROM aulas WHERE nombre=? ALLOW FILTERING;')#PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
            rows = session.execute(query, [aulanombre]) #EJECUTO LA QUERY Y LE PASO LAS VARIABLES PARA FILTRAR IMPORTANTE QUE ESTEN ENTRE CORCHETES
            existen = [] #CREO UN ARRAY
            for row in rows:
                existen.append(row) #LLENO EL ARRAY CON LAS FILAS
            cluster.shutdown() # Cierro La conexion
            if len(existen) > 0: 
                return HttpResponse("El aula {} ya existe".format(aulanombre))

            else:
                #agregar un dia y crear las aulas x 5

                crearaulas(aulanombre,aulacapa,aulapiso)
                cluster.shutdown() # Cierro La conexion
                
                return HttpResponse("CREASTE UN AULA")

        # if a GET (or any other method) we'll create a blank form
    else:

        form = AulasForm()


    return render(request, 'aula.html', {'form': form})

