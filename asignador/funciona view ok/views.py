# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
import uuid
from asignador.forms import cursadasForm

#IMPORTS PARA QUE FUNCIONE EL DRIVER CON CASSANDRA

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from cursadas.models import cursadas
from aulas.models import aulas
#from django.db import connection
from django.http import HttpResponse 
from cassandra.cqlengine import columns
from collections import namedtuple


def lista(vv):
    for v in vv:
        print(v)

def get_asignador(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = cursadasForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # allcursadas = cursadas.objects.filter(cantalumnos = 1231)
             #allaulas= aulas.objects.all()
             #cursor = connection.cursor()
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            session.set_keyspace('dbpwa')
            session.execute("truncate dbpwa.planificacion ")
            cluster.shutdown()

             #allaulas = cursor.execute("SELECT * FROM aulas WHERE nombre = 'MAGNA' ALLOW FILTERING;") # refiero los values con el comodin %s luego le clavo las variables
            

             #data = request.POST.copy() # Copia la data del post a la variable data, luego voy a extaer los campos del form con esta variable
             # cantalumnosint = int(cantalumnos) #lo fuerzo a int porque nose porque piensa que es un int, sin esta conversion falla el insert
             # carrera = data.get('carrera') #esto refiere al nombre que definimos en el form.py
             #comision = data.get('comision') #esto refiere al nombre que definimos en el form.py
             # horario = data.get('horario') #esto refiere al nombre que definimos en el form.py
             # nombremat = data.get('nombremat') #esto refiere al nombre que definimos en el form.py
             #turno = data.get('turno') #esto refiere al nombre que definimos en el form.py
             #cluster = Cluster(['127.0.0.1'])
             #session = cluster.connect()
             #session.set_keyspace('dbpwa')
             #query = session.prepare('SELECT * FROM cursadas WHERE comision=? AND turno=? ALLOW FILTERING;')#PREARMO LA QUERY EL ? SE REEMPLAZARA POR LAS VARIABLES
             #rows = session.execute(query, [comision, turno]) #EJECUTO LA QUERY Y LE PASO LAS VARIABLES PARA FILTRAR IMPORTANTE QUE ESTEN ENTRE CORCHETES
            aularows = aulas.objects.all()
            allaulas = []
            for row in aularows:
               allaulas.append(row)

            cursadarows = cursadas.objects.all()
            allcursadas = []
            for row in cursadarows:
               allcursadas.append(row)
     
            aulas_ordenadas=sorted(allaulas,key=lambda aulas:aulas.capacidad)
            cursadas_ordenadas=sorted(allcursadas,key=lambda cursadas:cursadas.cantalumnos,reverse=True)

            for x in range(len(aulas_ordenadas)):
                if len(cursadas_ordenadas)>0:
                    aula_usada=False
                    for y in range(len(cursadas_ordenadas)):
                        if aulas_ordenadas[x].capacidad>=cursadas_ordenadas[y].cantalumnos:
                            print('aula nro:',aulas_ordenadas[x].nombre,'cursada:',cursadas_ordenadas[y].nombremat)
                            #INICIO DE LOGICA DE INSERCION EN DB
                            cluster = Cluster(['127.0.0.1'])
                            session = cluster.connect()
                            session.set_keyspace('dbpwa')
                            session.execute("INSERT INTO planificacion(planificacion_id, carrera, nombremat, comision, turno, aula, piso) VALUES (%s,%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursadas_ordenadas[y].carrera, cursadas_ordenadas[y].nombremat, cursadas_ordenadas[y].comision, cursadas_ordenadas[y].turno, aulas_ordenadas[x].nombre, aulas_ordenadas[x].piso))
                            cluster.shutdown()
                            #FIN DE LOGICA DE INSERCION EN DB

                            cursadas_ordenadas.pop(y)
                            aula_usada=True
                            break
                    if aula_usada==False:
                        print('AULA SIN USAR:',aulas_ordenadas[x].nombre)
                        #INICIO DE LOGICA DE INSERCION EN DB
                        cluster = Cluster(['127.0.0.1'])
                        session = cluster.connect()
                        session.set_keyspace('dbpwa')
                        session.execute("INSERT INTO aulasinuso(aulasinuso_id, nombre, capacidad, piso) VALUES (%s,%s,%s,%s)",(uuid.uuid1(), aulas_ordenadas[x].nombre, aulas_ordenadas[x].capacidad, aulas_ordenadas[x].piso))
                        cluster.shutdown()
                        #FIN DE LOGICA DE INSERCION EN DB
                                                    
            if len(cursadas_ordenadas)>0:
                print('MATERIA SIN AULA:')
                for z in range(len(cursadas_ordenadas)):
                    cluster = Cluster(['127.0.0.1'])
                    session = cluster.connect()
                    session.set_keyspace('dbpwa')
                    session.execute("INSERT INTO cursadasinaula(cursadasinaula_id, carrera, nombremat, cantalumnos, comision, turno) VALUES (%s,%s,%s,%s,%s,%s)",(uuid.uuid1(), cursadas_ordenadas[z].carrera, cursadas_ordenadas[z].nombremat,cursadas_ordenadas[z].cantalumnos, cursadas_ordenadas[z].comision, cursadas_ordenadas[z].turno))
                    cluster.shutdown() 

                      
                #lista(cursadas_ordenadas)

            return HttpResponse('OK')

    # if a GET (or any other method) we'll create a blank form
    else:

        form = cursadasForm()


    return render(request, 'asignador.html', {'form': form})


 